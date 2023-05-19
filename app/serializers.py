import pytz
from datetime import datetime, timezone, timedelta

from rest_framework import serializers

from celery.result import AsyncResult

from .models import Client, Mailing, MailingStats
from .utils import validate_phone_number
from app.service.mailing import send_mailing
from .tasks import send_postponed_mailing, update_messages_stats

from main.celery import app


class ClientSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20, required=True)
    operator_code = serializers.CharField(read_only=True)
    tag = serializers.CharField(max_length=20, required=False)
    tz = serializers.CharField(max_length=20, required=False, default='UTC')

    def validate(self, attrs):

        if Client.objects.filter(phone_number=attrs.get('phone_number')).exists():
            raise serializers.ValidationError("Client with this phone number already exists")
        phone_number = attrs.get('phone_number')

        if phone_number:

            is_valid, operator_code, complete_number = validate_phone_number(phone_number)

            if not is_valid:
                raise serializers.ValidationError("Invalid phone number")

            attrs['operator_code'] = operator_code
            attrs["phone_number"] = complete_number

        try:
            pytz.timezone(attrs.get('tz'))
        except pytz.exceptions.UnknownTimeZoneError:
            raise serializers.ValidationError("Invalid timezone")

        return attrs

    def create(self, validated_data):
        return Client.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.operator_code = validated_data.get('operator_code', instance.operator_code)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.tz = validated_data.get('tz', instance.tz)
        instance.save()
        return instance


class MailingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(required=True)
    sent_at = serializers.DateTimeField(read_only=True)
    tag = serializers.CharField(max_length=20, required=False)
    operator_code = serializers.CharField(max_length=10, required=False)

    class Meta:
        model = Mailing
        fields = ('id', 'created_at', 'sent_at', 'body', 'operator_code', 'tag')

    def validate(self, attrs):

        created_at = attrs.get('created_at')
        if not created_at:
            attrs['created_at'] = datetime.now()

        operator_code = attrs.get('operator_code')

        if not operator_code:
            return attrs

        if not operator_code.isdigit():
            raise serializers.ValidationError("Invalid format of the operator code. Should be a number")

        return attrs

    def create(self, validated_data):

        mailing = Mailing.objects.create(**validated_data)

        # start the mail out immediately and save the "sent_at" once the sent-out is completed
        if validated_data.get("created_at") < datetime.now(timezone.utc):
            send_mailing(mailing)
            sent_at = datetime.now()
            mailing.sent_at = sent_at
            mailing.save()
            stats_table = MailingStats.objects.get(mailing_id=mailing.id)
            stats_table.completed = True
            stats_table.save()

        # start the mail out at "created_at" and save the "sent_at" once the sent-out is completed
        else:
            execution_time = validated_data.get("created_at")
            result = send_postponed_mailing.apply_async(args=(mailing.id,), eta=execution_time)
            update_messages_stats.apply_async(args=(result.task_id, mailing.id,), eta=execution_time + timedelta(minutes=2))

        return mailing

    def update(self, instance, validated_data):
        instance.sent_at = validated_data.get('sent_at', instance.sent_at)
        instance.body = validated_data.get('body', instance.body)
        instance.operator_code = validated_data.get('operator_code', instance.operator_code)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.save()
        return instance


class MailingStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingStats
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MailingStats
        fields = ('id', 'mailing_id', 'status', 'created_at', 'updated_at', 'completed', 'task_id')

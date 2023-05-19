import phonenumbers

from rest_framework import serializers

from .country_codes import MNC_COUNTRY_CODES, MNC_COUNTRY_DIGITS


def validate_phone_number(number):
    try:
        parsed_number = phonenumbers.parse(number, None)

        # Validating the number (its format)
        if not phonenumbers.is_valid_number(parsed_number):
            raise serializers.ValidationError('Invalid phone number')

        # Getting the country of origin of the number
        country_code = MNC_COUNTRY_CODES[str(parsed_number.country_code)]

        # Checking if the country is in our default list of countries
        if country_code in MNC_COUNTRY_DIGITS:
            mnc_digits = MNC_COUNTRY_DIGITS[country_code]

        # return if the number is valid and country of origin is None
        else:
            complete_number = "+" + str(parsed_number.country_code) + str(parsed_number.national_number)
            return True, None, complete_number

        mnc = str(parsed_number.national_number)[0:mnc_digits]

        complete_number = "+" + str(parsed_number.country_code) + str(parsed_number.national_number)

        return True, mnc, complete_number

    except Exception as e:
        raise serializers.ValidationError("Couldn't parse the phone number")

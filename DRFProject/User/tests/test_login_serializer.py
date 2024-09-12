import pytest
from User.serializers import LoginSerializer
from rest_framework.serializers import ValidationError


@pytest.mark.parametrize(
    'data, is_valid, expected_errors',
    [
        (
            {'email': 'testuser@example.com', 'password': 'password123'},
            True,
            {}
        ),
        (
            {'email': 'invalidemail', 'password': 'password123'},
            False,
            {'email': ['Enter a valid email address.']}
        ),
        (
            {'email': 'testuser@example.com'},
            False,
            {'password': ['This field is required.']}
        ),
        (
            {'password': 'password123'},
            False,
            {'email': ['This field is required.']}
        ),
        (
            {},
            False,
            {
                'email': ['This field is required.'],
                'password': ['This field is required.']
            }
        ),
    ]
)
def test_login_serializer(data: dict[str, str], is_valid: bool,
                          expected_errors):
    serializer = LoginSerializer(data=data)

    assert serializer.is_valid() == is_valid

    if not is_valid:
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
        assert serializer.errors == expected_errors
    else:
        assert serializer.validated_data == data

RESET_PASSWORD = '''
<!DOCTYPE html>
<html style="width: 100vw; height: 100vh; overflow-x: hidden;">
    <head>
        <title>Form for reset password</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta charset="utf-8">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" 
        rel="preload" as="style" onload="this.rel='stylesheet'; this.onload=null">
    </head>
    <body style="width: inherit; height: inherit; display: flex; align-items: center; justify-content: center; 
    font-family: 'Montserrat', sans-serif; margin: 0; box-sizing: border-box; padding: 50px;
    background-image: linear-gradient(62deg, #8EC5FC 0%, #E0C3FC 100%);">
        <form method="POST" action="{url}"
        style="display: flex; flex-direction: column; align-items: center; row-gap: 8vh;">
            <h1 style="color: #3F3D56; font-size: 48px; margin: 0; margin-bottom: 5vh; text-align: center;">
                Form for reset password
            </h1>
            <div style="display: flex; column-gap: 3vw; align-items: center;">
                <label for="new_password" style="color: #3F3D56;
                font-size: 20px; font-weight: 500; text-align: center;">
                    Your new password:
                </label>
                <input type="password" id="new_password" name="password" required
                style="box-sizing: border-box; padding: 1.5vh 4.5vw; border-radius: 10px; font-size: 20px;
                border: none; background-color: #3F3D56; color: #9e9cae; outline: none;">
            </div>
            <button type="submit" style="box-sizing: border-box; padding: 2vh 4.5vw; border-radius: 10px;
            cursor: pointer; border:none; background-color: #FF6B6B; color: #3F3D56;
            font: inherit; font-size: 20px; font-weight: 700;">
                Change Password
            </button>
        </form>
    </body>
</html>'''

EMAIL_RESET_PASSWORD = '''
<!DOCTYPE html>
<html>
    <body style="margin: 0; padding: 0; width: 100%; height: 100%;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="padding: 25px;">
            <tr>
                <td align="center">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0"
                    style="background-color: #3F3D56; border-radius: 10px; min-height: 250px;">
                        <tr>
                            <td align="center" style="padding: 50px;">
                                <h1 style="color: white; margin: 0; margin-bottom: 75px;
                                font-family: 'Helvetica', sans-serif; font-size: 22px; font-weight: 600;">
                                    Someone just requested to reset your password. If it was you, click on the link below:
                                </h1>
                                <a href="{url}" style="background-color: #7e2a1f; color: white; box-sizing: 
                                border-box; padding: 2vh 4vw; text-decoration: none; border-radius: 10px;
                                font-family: 'Helvetica', sans-serif; font-size: 20px;">
                                    Reset Password
                                </a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>'''

EMAIL_CONFIRM_ORDER = '''
<!DOCTYPE html>
<html>
    <body style="margin: 0; padding: 0; width: 100%; height: 100%;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="padding: 25px;">
            <tr>
                <td align="center">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0"
                    style="background-color: #3F3D56; border-radius: 10px; min-height: 250px;">
                        <tr>
                            <td align="center" style="padding: 50px;">
                                <h1 style="color: white; margin: 0; margin-bottom: 75px;
                                font-family: 'Helvetica', sans-serif; font-size: 22px; font-weight: 600;">
                                    You just recently created an order, please confirm it by clicking on the link below:
                                </h1>
                                <a href="{url}" style="background-color: #eacd3f; color: black; box-sizing: 
                                border-box; padding: 2vh 4vw; text-decoration: none; border-radius: 10px;
                                font-family: 'Helvetica', sans-serif; font-size: 20px;">
                                    Confirm Order
                                </a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>'''

EMAIL_FOR_ADMIN = '''
<!DOCTYPE html>
<html>
    <body style="margin: 0; padding: 0; width: 100%; height: 100%;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="padding: 25px;">
            <tr>
                <td align="center">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0"
                    style="background-color: #3F3D56; border-radius: 10px; min-height: 250px;">
                        <tr>
                            <td align="center" style="padding: 50px;">
                                <h1 style="color: white; margin: 0; margin-bottom: 75px;
                                font-family: 'Helvetica', sans-serif; font-size: 22px; font-weight: 600;">
                                    {user} confirmed his order and he is waiting for delivery. He ordered:
                                </h1>
                                <ul style="text-align: left; font-size: 18px; color: white">
                                    {user_order}
                                </ul>
                                <h2 style="color: white">Overall Price is {overall_price}</h2>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>'''

EMAIL_CONFIRM_EMAIL = '''
<!DOCTYPE html>
<html>
    <body style="margin: 0; padding: 0; width: 100%; height: 100%;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="padding: 25px;">
            <tr>
                <td align="center">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0"
                    style="background-color: #3F3D56; border-radius: 10px; min-height: 250px;">
                        <tr>
                            <td align="center" style="padding: 50px;">
                                <h1 style="color: white; margin: 0; margin-bottom: 75px;
                                font-family: 'Helvetica', sans-serif; font-size: 22px; font-weight: 600;">
                                    Please confirm your email address by clicking on the link below:
                                </h1>
                                <a href="{url}" style="background-color: #4CAF50; color: black; box-sizing: 
                                border-box; padding: 2vh 4vw; text-decoration: none; border-radius: 10px;
                                font-family: 'Helvetica', sans-serif; font-size: 20px;">
                                    Confirm Email
                                </a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>'''
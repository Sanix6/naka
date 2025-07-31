EMAIL_TEMPLATE = """
<div style="font-family: Arial, sans-serif; padding: 20px;">
    <h2 style="color: #333;">Добро пожаловать, {first_name}!</h2>
    <p>Ваш код подтверждения: <strong style="font-size: 20px;">{code}</strong></p>
    <p>Введите этот код в приложении, чтобы завершить регистрацию.</p>
    <br>
    <p>С уважением,<br>Ваша команда</p>
</div>
"""


NEWPASSWORD_TEMPLATE = """
<html>
  <body style="margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; background-color: #f4f6f8;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tr>
        <td align="center" style="padding: 40px 0;">
          <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="600" style="background: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);">
            <tr>
              <td style="padding: 40px; text-align: left;">
                <h1 style="margin: 0 0 24px 0; font-size: 24px; color: #1a1a1a;">Сброс пароля</h1>
                <p style="font-size: 16px; color: #4d4d4d; margin-bottom: 24px;">
                  Здравствуйте, {first_name},
                </p>
                <p style="font-size: 16px; color: #4d4d4d; margin-bottom: 24px;">
                  Мы получили запрос на сброс пароля для вашей учетной записи. Чтобы создать новый пароль, нажмите на кнопку ниже:
                </p>
                <p style="text-align: center; margin: 30px 0;">
                  <a href="{reset_url}" style="background-color: #1a73e8; color: #ffffff; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-weight: 500; font-size: 16px; display: inline-block;">
                    Установить новый пароль
                  </a>
                </p>
                <p style="font-size: 14px; color: #999999; margin-top: 40px;">
                  Ссылка действительна в течение 15 минут. Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.
                </p>
              </td>
            </tr>
            <tr>
              <td style="background: #f0f0f0; padding: 20px; text-align: center; font-size: 13px; color: #888888;">
                © 2025 NAKA. Все права защищены.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""






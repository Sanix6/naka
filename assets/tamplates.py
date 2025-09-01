EMAIL_TEMPLATE = """
<div style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 30px;">
    <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); overflow: hidden;">
        
        <div style="background: linear-gradient(135deg, #03A39E, #00d6d0); padding: 20px; text-align: center;">
            <h1 style="margin: 0; font-size: 24px; color: #ffffff; font-weight: bold;">naka.kz</h1>
        </div>
        
        <div style="padding: 25px; color: #333;">
            <h2 style="color: #222;">Добро пожаловать, {first_name}!</h2>
            <p style="font-size: 16px; line-height: 1.5;">
                Спасибо, что присоединились к <strong>naka.kz</strong>.  
                Для завершения регистрации используйте код ниже:
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <span style="display: inline-block; font-size: 26px; font-weight: bold; letter-spacing: 4px; background: #f1f5ff; color: #03A39E; padding: 12px 20px; border-radius: 8px;">
                    {code}
                </span>
            </div>
            
            <p style="font-size: 14px; color: #555;">
                Введите этот код в приложении, чтобы подтвердить ваш аккаунт.  
                Код действует ограниченное время.
            </p>
            
            <br>
            <p style="font-size: 14px; color: #777;">С уважением,<br>Команда <strong>naka.kz</strong></p>
        </div>
    </div>
</div>
"""



NEWPASSWORD_TEMPLATE = """
<html>
  <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6f8;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tr>
        <td align="center" style="padding: 40px 0;">
          <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="600" 
                 style="background: #ffffff; border-radius: 12px; overflow: hidden; 
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);">
            
            <!-- Шапка -->
            <tr>
              <td style="background: linear-gradient(135deg, #03A39E, #00d6d0); padding: 20px; text-align: center;">
                <h1 style="margin: 0; font-size: 22px; color: #ffffff; font-weight: bold;">naka.kz</h1>
              </td>
            </tr>
            
            <!-- Контент -->
            <tr>
              <td style="padding: 40px; text-align: left;">
                <h2 style="margin: 0 0 24px 0; font-size: 24px; color: #1a1a1a;">Сброс пароля</h2>
                
                <p style="font-size: 16px; color: #4d4d4d; margin-bottom: 24px;">
                  Здравствуйте, {first_name},
                </p>
                
                <p style="font-size: 16px; color: #4d4d4d; margin-bottom: 28px;">
                  Мы получили запрос на сброс пароля для вашей учетной записи.  
                  Чтобы создать новый пароль, нажмите на кнопку ниже:
                </p>
                
                <p style="text-align: center; margin: 35px 0;">
                  <a href="{reset_url}" 
                     style="background-color: #03A39E; color: #ffffff; text-decoration: none; 
                            padding: 14px 32px; border-radius: 8px; font-weight: 600; 
                            font-size: 16px; display: inline-block; box-shadow: 0 3px 8px rgba(3,163,158,0.3);">
                    Установить новый пароль
                  </a>
                </p>
                
                <p style="font-size: 14px; color: #888888; margin-top: 40px; line-height: 1.6;">
                  🔒 Ссылка действительна в течение <strong>15 минут</strong>.  
                  Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.
                </p>
              </td>
            </tr>
            
            <!-- Подвал -->
            <tr>
              <td style="background: #f0f0f0; padding: 18px; text-align: center; font-size: 13px; color: #777777;">
                © 2025 <strong>naka.kz</strong>. Все права защищены.
              </td>
            </tr>
            
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""

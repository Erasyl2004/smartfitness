from app.interfaces.templates.otp import OtpTemplate
from dataclasses import dataclass
from typing import ClassVar
import textwrap


@dataclass(eq=False)
class OtpTemplateImpl(OtpTemplate):
    template: ClassVar[str] = textwrap.dedent(
        """
        <!DOCTYPE html>
        <html lang="ru">
        
        <head>
            <meta charset="UTF-8">
            <title>Подтверждение почты</title>
        </head>
        
        <body style="margin:0; padding:0; background-color:#f4f6f8; font-family: Arial, sans-serif;">
        
            <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                    <td align="center" style="padding: 40px 0;">
        
                        <!-- Main Card -->
                        <table width="400" cellpadding="0" cellspacing="0"
                            style="background:#ffffff; border-radius:12px; padding:30px; box-shadow:0 2px 10px rgba(0,0,0,0.1);">
        
                            <!-- Logo / Title -->
                            <tr>
                                <td align="center" style="padding-bottom:20px;">
                                    <h2 style="margin:0; color:#2c3e50;">Smart Fitness</h2>
                                </td>
                            </tr>
        
                            <!-- Text -->
                            <tr>
                                <td style="color:#333333; font-size:15px; line-height:1.5; padding-bottom:20px;">
                                    Привет! 👋 <br><br>
                                    Вы получили это письмо, потому что регистрируетесь в приложении <b>Smart Fitness</b>.
                                    Используйте код ниже для подтверждения вашей почты:
                                </td>
                            </tr>
        
                            <!-- OTP Code -->
                            <tr>
                                <td align="center" style="padding:20px 0;">
                                    <div style="
                        background:#f1f3f5;
                        padding:15px 25px;
                        border-radius:8px;
                        font-size:28px;
                        font-weight:bold;
                        letter-spacing:6px;
                        color:#111111;
                        display:inline-block;
                      ">
                                        {otp_code}
                                    </div>
                                </td>
                            </tr>
        
                            <!-- Warning -->
                            <tr>
                                <td style="color:#666666; font-size:13px; padding-bottom:20px;">
                                    Если вы не запрашивали этот код — просто проигнорируйте письмо.
                                </td>
                            </tr>
        
                            <!-- Footer -->
                            <tr>
                                <td align="center" style="color:#999999; font-size:12px;">
                                    © 2026 Smart Fitness<br>
                                    Все права защищены
                                </td>
                            </tr>
        
                        </table>
        
                    </td>
                </tr>
            </table>
        
        </body>
        
        </html>
        """
    )

    def from_template(self, otp_code: str) -> str:
        return self.template.format(otp_code=otp_code)

"""
file     Avatar_ATOMS3
time     2025-05-22
author   akita11
email   akita@ifdl.jp
license  MIT License
"""

import os, sys, io
import M5
from M5 import *
from machine import Timer
from hardware import Pin
from hardware import ADC
import random
import math
import time

class HelloATOMS3:
    """
    note:
        en: ''
    details:
        color: '#0fb1d2'
        link: ''
        image: ''
        category: Custom
    example: ''
    """




    def __init__(self):
        """
        label:
            en: '%1 init'
        """
        self.face_color_bg = 0x000000
        self.face_color_fg = 0xffffff
        self.face_color_text = 0x00ff00
        self.SCREEN_W, self.SCREEN_H = 128, 128
        self.EYE_X, self.EYE_Y, self.EYE_R = 32, 42, 6
        self.EYE_CLOSE_W, self.EYE_CLOSE_H = 10, 3
        self.MOUTH_W, self.MOUTH_H, self.MOUTH_H_OPEN = 48, 4, 14
        # MOUTH_CLOSE_H = 10
        self.MOUTH_X, self.MOUTH_Y = (self.SCREEN_W - self.MOUTH_W) // 2, 93
        self.EXCLAM_X, self.EXCLAM_Y = 120, 5
        self.EXCLAM_W, self.EXCLAM_H, self.EXCLAM_SPC = 5, 20, 5
        self.PALE_X, self.PALE_Y = 105, 5
        self.PALE_W, self.PALE_H, self.PALE_H_DIFF, self.PALE_SPC = 3, 20, 3, 6
        self.FONT_W, self.FONT_H = 24, 24
        self.fFaceStatus = 0
        self.isMouthClosed = True
        self.timer_avatar = Timer(0)
        self.tm_blink = 0
        self.st_blink = 0
        self.tm_blink_open = random.randint(2, 6) * 1000
        self.timer_interval = 100  # [ms]
        self.st_mouth = 0
        self.fSpeak = False
        self.tm_mouth = 0
        self.st_mouth = 0
        self.timer_mouth_interval = 500 # [ms]
        self.text_speech = ''
        self.dev = 0
        self.breath_T = 0
        self.breath_cycle = 30
        self.breath_dev = 4
        Display.setFont(M5.Lcd.FONTS.EFontJA24)
        Display.fillScreen(self.face_color_bg)
        self._draw_eye_open()
        self._draw_mouth_close()
        self.timer_avatar.init(period=self.timer_interval, mode=Timer.PERIODIC, callback=self._avatar_timer)
        self._LED = Pin(5, mode=Pin.OUT)
        self._Light = ADC(Pin(6), atten=ADC.ATTN_11DB)
        pass

    def FaceSmile(self):
        """
        label:
            en: SmileFace %1
        """
        #global self.fFaceStatus
        self.fFaceStatus = 1
        pass

    def FaceSleepy(self):
        """
        label:
            en: SleepyFace %1
        """
        #global self.fFaceStatus
        self.fFaceStatus = 2
        pass

    def FaceNormal(self):
        """
        label:
            en: NormalFace %1
        """
        #global self.fFaceStatus
        self.fFaceStatus = 0
        pass

    def Exclamation(self, Enable):
        """
        label:
            en: Exclamation %1 %2
        params:
            Enable:
                name: Enable
                field: dropdown
                options:
                    'ON': enable
                    'OFF': disable
        """
        if (Enable == 1):
            self.color = 0xff0000 # red
        else:
            self.color = self.face_color_bg
        Display.fillRect(self.EXCLAM_X, self.EXCLAM_Y, self.EXCLAM_W, self.EXCLAM_H, self.color)
        Display.fillRect(self.EXCLAM_X, self.EXCLAM_Y + self.EXCLAM_H + self.EXCLAM_SPC, self.EXCLAM_W, self.EXCLAM_W, self.color)
        pass

    def Pale(self, Enable):
        """
        label:
            en: Pale %1 %2
        params:
            Enable:
                name: Enable
                field: dropdown
                options:
                    'ON': enable
                    'OFF': disable
        """
        if (Enable == 1):
            self.color = 0x0000ff # blue
        else:
            self.color = self.face_color_bg
        for i in range(4):
            Display.fillRect(self.PALE_X + self.PALE_SPC * i, self.PALE_Y, self.PALE_W, self.PALE_H - self.PALE_H_DIFF * i, self.color)
        pass

    def FaceColor(self, color: int = 0xFF0000):
        """
        label:
            en: FaceColor %1 %2
        params:
            color:
                name: color
                type: int
                default: '0xFF0000'
                field: colour
        """
        #global self.face_color
        self.face_color_bg = color
        Display.fillScreen(self.face_color_bg)
        self._draw_eye_open()
        self._draw_mouth_close()

        pass

    def _breath(self):
        """
        label:
            en: ' %1 _breath'
        """
        global dev, breath_T
        self.breath_T = (self.breath_T + 1) % self.breath_cycle
        self.dev = int(self.breath_dev * math.sin(self.breath_T * 2 * math.pi / self.breath_cycle))

    def _draw_eye_open(self):
        """
        label:
            en: ' %1 _draw_eye_open'
        """
        if self.fFaceStatus == 0:
            # normal
            Display.fillCircle(                self.EYE_X, self.EYE_Y + self.dev, self.EYE_R, self.face_color_fg)
            Display.fillCircle(self.SCREEN_W - self.EYE_X, self.EYE_Y + self.dev, self.EYE_R, self.face_color_fg)
        elif self.fFaceStatus == 1:
            # smile
            Display.fillArc(                self.EYE_X, self.EYE_Y + self.dev, self.EYE_R + 2, self.EYE_R - 2, 180, 360, self.face_color_fg)
            Display.fillArc(self.SCREEN_W - self.EYE_X, self.EYE_Y + self.dev, self.EYE_R + 2, self.EYE_R - 2, 180, 360, self.face_color_fg)
        else:
            #sleep
            Display.fillArc(                self.EYE_X, self.EYE_Y + self.dev, self.EYE_R + 2, self.EYE_R - 2, 0, 180, self.face_color_fg)
            Display.fillArc(self.SCREEN_W - self.EYE_X, self.EYE_Y + self.dev, self.EYE_R + 2, self.EYE_R - 2, 0, 180, self.face_color_fg)

    def _draw_eye_close(self):
        """
        label:
            en: ' %1 _draw_eye_close'
        """
        Display.fillRect(                self.EYE_X - self.EYE_CLOSE_W//2, self.EYE_Y - self.EYE_CLOSE_H//2 + self.dev, self.EYE_CLOSE_W, self.EYE_CLOSE_H, self.face_color_fg)
        Display.fillRect(self.SCREEN_W - self.EYE_X - self.EYE_CLOSE_W//2, self.EYE_Y - self.EYE_CLOSE_H//2 + self.dev, self.EYE_CLOSE_W, self.EYE_CLOSE_H, self.face_color_fg)

    def _clear_eyes(self):
        """
        label:
            en: ' %1 _clear_eyes'
        """
        Display.fillRect(               self.EYE_X - self.EYE_R - 3, self.EYE_Y - self.EYE_R - 4 + self.dev, self.EYE_R*2 + 6, self.EYE_R*2 + 8, self.face_color_bg)
        Display.fillRect(self.SCREEN_W- self.EYE_X - self.EYE_R - 3, self.EYE_Y - self.EYE_R - 4 + self.dev, self.EYE_R*2 + 6, self.EYE_R*2 + 8, self.face_color_bg)

    def _draw_mouth_open(self):
        """
        label:
            en: ' %1 _draw_mouth_open'
        """
        Display.fillRect(self.MOUTH_X, self.MOUTH_Y - self.MOUTH_H_OPEN // 2, self.MOUTH_W, self.MOUTH_H_OPEN, self.face_color_fg)

    def _draw_mouth_close(self):
        """
        label:
            en: ' %1 _draw_mouth_close'
        """
        Display.fillRect(self.MOUTH_X, self.MOUTH_Y - self.MOUTH_H // 2, self.MOUTH_W, self.MOUTH_H, self.face_color_fg)

    def _clear_mouth(self):
        """
        label:
            en: ' %1 _clear_mouth'
        """
        Display.fillRect(self.MOUTH_X-2, self.MOUTH_Y - self.MOUTH_H_OPEN // 2 - 2, self.MOUTH_W+4, self.MOUTH_H_OPEN + 4, self.face_color_bg)

    def _avatar_timer(self, timer):
        """
        label:
            en: ' %1 _avatar_timer, timer: %2'
        params:
            timer:
                name: timer
        """
        global tm_blink, st_blink, tm_blink_open, tm_mouth, st_mouth, fSpeak, text_speech
        self._breath()
        self.tm_blink += self.timer_interval
        self._clear_eyes()
        if self.st_blink == 0:
            if self.fFaceStatus != 2: # normal or smile
                self._draw_eye_close()
            if self.tm_blink >= 300:
                self.st_blink = 1
                self.tm_blink = 0
        else:
            self._draw_eye_open()
            if self.tm_blink >= self.tm_blink_open:
                self.tm_blink_open = random.randint(2, 6) * 1000
                self.st_blink = 0
                self.tm_blink = 0

    def Speak(self, text: str = 'Hello'):
        """
        label:
            en: Speak %1 %2
        params:
            text:
                name: text
                type: str
                default: Hello
        """
        global fSpeak, tm_mouth, text_speech
        Display.drawArc(self.FONT_W, self.SCREEN_H - self.FONT_H, self.FONT_W, self.FONT_H, 180, 270, self.face_color_text)
        Display.drawLine(0, self.SCREEN_H-1 - self.FONT_H, 0, self.SCREEN_H-1, self.face_color_text)
        Display.drawLine(0, self.SCREEN_H-1, self.SCREEN_W-1, self.SCREEN_H-1, self.face_color_text)
        Display.drawLine(self.SCREEN_W-1, self.SCREEN_H, self.SCREEN_W-1, self.SCREEN_H - self.FONT_H, self.face_color_text)
        Display.drawLine(self.SCREEN_W-1, self.SCREEN_H - self.FONT_H, self.FONT_H, self.SCREEN_H - self.FONT_H, self.face_color_text)
        Display.drawLine(self.FONT_W, self.SCREEN_H - 2*self.FONT_H, self.FONT_W, self.SCREEN_H - self.FONT_H, self.face_color_text)
        Display.fillRect(1, self.SCREEN_H - self.FONT_H + 1, self.SCREEN_W - 2, self.FONT_H - 2, self.face_color_bg)
        Display.setCursor(0, self.SCREEN_H - self.FONT_H)
        Display.print(text, color=self.face_color_text)
        self.text_speech = text
        self.st_mouth = 0

        for i in range(len(text)):
            time.sleep_ms(500)
            self.st_mouth = (self.st_mouth + 1) % 2
            if self.st_mouth == 1:
                self._clear_mouth()
                self._draw_mouth_open()
            else:
                self._clear_mouth()
                self._draw_mouth_close()
            self.text_speech = self.text_speech[1:]
            Display.fillRect(1, self.SCREEN_H - self.FONT_H + 1, self.SCREEN_W - 2, self.FONT_H - 2, self.face_color_bg)
            Display.setCursor(0, self.SCREEN_H - self.FONT_H)
            Display.print(self.text_speech, color=self.face_color_text)

        Display.fillRect(0, self.SCREEN_H - 2*self.FONT_H, self.FONT_W+1, self.FONT_H, self.face_color_bg)
        Display.fillRect(0, self.SCREEN_H - self.FONT_H, self.SCREEN_W, self.FONT_H, self.face_color_bg)
        self._clear_mouth()
        self._draw_mouth_close()
        time.sleep_ms(500)

    def SetLED(self, val: int = 0):
        """
        label:
            en: SetLED %1 %2
        params:
            val:
                name: val
                type: int
                default: '0'
                field: number
                max: '100'
                min: '0'
        """
        self._LED.value(val)
        pass

    def GetLight(self):
        """
        label:
            en: GetLight %1
        """
        return(int(self._Light.read() / 4095 * 100))
        pass



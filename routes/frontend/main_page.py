'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-11-29 20:04:24
FilePath: /Findreve/main_page.py
Description: Findreve 个人主页 main_page

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

from nicegui import ui
from fastapi import Request
import logging
import requests
import json
import model


def create() -> None:
    @ui.page('/')
    async def main_page(request: Request) -> None:

        dark_mode = ui.dark_mode(value=True)

        with ui.row(align_items='center').classes('w-full items-center justify-center items-stretch mx-auto mx-8 max-w-7xl p-24'):
            with ui.column(align_items='center').classes('px-2 max-md:hidden'):
                ui.chip('🐍 Python 是最好的语言').classes('text-xs -mt-1 -right-3').props('floating outline')
                ui.chip('🎹 精通 FL Studio Mobile').classes('text-xs -mt-1').props('floating outline')
                ui.chip('🎨 熟悉 Ps/Pr/Ae/Au/Ai').classes('text-xs -mt-1').props('floating outline')
                ui.chip('🏎 热爱竞速(如地平线5)').classes('text-xs -mt-1 -right-3').props('floating outline')
            with ui.avatar().classes('w-32 h-32 transition-transform duration-300 hover:scale-110 cursor-pointer'):
                # 下面的这个是Base64格式，你需要改成你自己的头像，支持链接，也可以用Base64本地化
                ui.image('/static/heyfun.jpg').classes('w-32 h-32')
            with ui.column().classes('px-2 max-md:hidden'):
                ui.chip('喜欢去广州图书馆看书 📕').classes('text-xs -mt-1 -left-3').props('floating outline')
                ui.chip('致力做安卓苹果开发者 📱').classes('text-xs -mt-1').props('floating outline')
                ui.chip('正在自研全链个人生态 🔧').classes('text-xs -mt-1').props('floating outline')
                ui.chip('致力与开源社区同发展 🤝').classes('text-xs -mt-1 -left-3').props('floating outline')

        ui.label('关于本站').classes('w-full text-4xl text-bold text-center py-6 subpixel-antialiased')

        with ui.row().classes('w-full items-center justify-center items-stretch mx-auto mx-8 max-w-7xl py-4'):
            with ui.card().classes('w-full sm:w-1/5 lg:w-1/7 flex-grow p-8 bg-gradient-to-br from-indigo-700 to-blue-500'):
                ui.label('你好，很高兴认识你👋').classes('text-md text-white')
                with ui.row(align_items='center'):
                    ui.label('我叫').classes('text-4xl text-bold text-white -mt-1 subpixel-antialiased')
                    ui.label('于小丘').classes('text-4xl text-bold text-white -mt-1 subpixel-antialiased').tooltip('英文名叫Yuerchu，也可以叫我海枫')
                ui.label('是一名 开发者、音乐人').classes('text-md text-white -mt-1')
            with ui.card().classes('w-full sm:w-1/2 lg:w-1/4 flex-grow flex flex-col justify-center'):
                ui.code('void main() {\n    printf("为了尚未完成的未来");\n}', language='c').classes('text-3xl max-[768px]:text-xl text-bold text-white flex-grow w-full h-full')

        with ui.row().classes('w-full items-center justify-center items-stretch mx-auto mx-8 max-w-7xl -mt-3'):
            with ui.card().classes('w-full sm:w-1/2 lg:w-1/4 flex-grow p-4'):
                ui.label('技能').classes('text-md text-gray-500')
                ui.label('开启创造力').classes('text-4xl text-bold -mt-1 right-4')

                with ui.row().classes('items-center'):
                    ui.chip('Python', color='amber-400').classes('p-4').props('floating').tooltip('Python是世界上最好的语言')
                    ui.chip('Kotlin', color='violet-400').classes('p-4').props('floating').tooltip('Kotlin给安卓开发APP')
                    ui.chip('Golang', color='sky-400').classes('p-4').props('floating').tooltip('Golang写后端')
                    ui.chip('Lua', color='blue-900').classes('p-4').props('floating').tooltip('用aLua给安卓开发，给罗技鼠标写鼠标宏')
                    ui.chip('c', color='red-400').classes('p-4').props('floating').tooltip('C写嵌入式开发')
                    ui.chip('FL Studio', color='orange-600').classes('p-4').props('floating').tooltip('FL Studio是世界上最好的宿主')
                    ui.chip('Photoshop', color='blue-950').classes('p-4').props('floating').tooltip('修图/抠图/画画一站通')
                    ui.chip('Premiere', color='indigo-900').classes('p-4').props('floating').tooltip('剪视频比较顺手，但是一开风扇狂转')
                    ui.chip('After Effects', color='indigo-950').classes('p-4').props('floating').tooltip('制作特效，电脑太烂了做不了太花的')
                    ui.chip('Audition', color='purple-900').classes('p-4').props('floating').tooltip('写歌做母带挺好用的')
                    ui.chip('Illustrator', color='amber-800').classes('p-4').props('floating').tooltip('自制字体和画动态SVG')
                    ui.chip('HTML', color='red-900').classes('p-4').props('floating').tooltip('前端入门三件套，不学这玩意其他学了没用')
                    ui.chip('CSS3', color='cyan-900').classes('p-4').props('floating').tooltip('. window{ show: none; }')
                    ui.chip('JavaScript', color='lime-900').classes('p-4').props('floating').tooltip('还在努力学习中，只会一些简单的')
                    ui.chip('git', color='amber-700').classes('p-4').props('floating').tooltip('版本管理是真好用')
                    ui.chip('Docker', color='sky-600').classes('p-4').props('floating').tooltip('容器化部署')
                    ui.chip('chatGPT', color='emerald-600').classes('p-4').props('floating').tooltip('文本助驾，写代码/写文章/写论文')
                    ui.chip('SAI2', color='gray-950').classes('p-4').props('floating').tooltip('入门绘画')
                    ui.chip('ips Draw', color='gray-900').classes('p-4').props('floating').tooltip('自认为是iOS端最佳绘画软件')
                    ui.chip('AutoCAD', color='gray-950').classes('p-4').props('floating').tooltip('画图/绘制电路图')
                    ui.chip('SolidWorks', color='gray-900').classes('p-4').props('floating').tooltip('画图/绘制3D模型')
                    ui.chip('EasyEDA', color='gray-950').classes('p-4').props('floating').tooltip('画图/绘制电路图')
                    ui.chip('KiCad', color='gray-900').classes('p-4').props('floating').tooltip('画图/绘制电路图')
                    ui.chip('Altium Designer', color='gray-950').classes('p-4').props('floating').tooltip('画图/绘制电路图')
                    ui.label('...').classes('text-md text-gray-500')
            with ui.card().classes('w-full sm:w-1/3 lg:w-1/6 flex-grow  flex flex-col justify-center'):
                ui.label('生涯').classes('text-md text-gray-500')
                ui.label('无限进步').classes('text-4xl text-bold -mt-1 right-4')

                with ui.timeline(side='right', layout='comfortable'):
                    ui.timeline_entry('那天，我买了第一台服务器，并搭建了我第一个Wordpress站点',
                                    title='梦开始的地方',
                                    subtitle='2022年1月21日')
                    ui.timeline_entry('准备从Cloudreve项目脱离，自建网盘系统DiskNext',
                                    title='自建生态计划开始',
                                    subtitle='2024年3月1日')
                    ui.timeline_entry('目前正在开发HeyAuth、Findreve、DiskNext',
                                    title='项目框架仍在研发中',
                                    subtitle='现在',
                                    icon='rocket')

                

        ui.label('我的作品').classes('w-full text-center text-2xl text-bold p-4')

        with ui.row().classes('w-full items-center justify-center items-stretch mx-auto mx-8 max-w-7xl'):
            with ui.card().classes('w-full sm:w-1/3 lg:w-1/5 flex-grow p-4'):
                with ui.row().classes('items-center w-full -mt-2'):
                    ui.label('DiskNext').classes('text-lg text-bold')
                    ui.chip('B端程序').classes('text-xs').props('floating')
                    ui.space()
                    ui.button(icon='open_in_new', on_click=lambda: (ui.navigate.to('https://pan.yxqi.cn'))).props('flat fab-mini')
                ui.label('一个基于NiceGUI的网盘系统，性能与Golang媲美').classes('text-sm -mt-3')
            with ui.card().classes('w-full sm:w-1/3 lg:w-1/5 flex-grow p-4'):
                with ui.row().classes('items-center w-full -mt-2'):
                    ui.label('Findreve').classes('text-lg text-bold')
                    ui.chip('C端程序').classes('text-xs').props('floating')
                    ui.space()
                    ui.button(icon='open_in_new', on_click=lambda: (ui.navigate.to('https://i.yxqi.cn'))).props('flat fab-mini')
                ui.label('一个基于NiceGUI的个人主页配合物品丢失找回系统').classes('text-sm -mt-3')
            with ui.card().classes('w-full sm:w-1/3 lg:w-1/5 flex-grow p-4'):
                with ui.row().classes('items-center w-full -mt-2'):
                    ui.label('HeyAuth').classes('text-lg text-bold')
                    ui.chip('B端程序').classes('text-xs').props('floating')
                    ui.space()
                    ui.button(icon='open_in_new', on_click=lambda: (ui.navigate.to('https://auth.yxqi.cn'))).props('flat fab-mini')
                ui.label('一个基于NiceGUI的B+C端多应用授权系统').classes('text-sm -mt-3')

        with ui.row().classes('w-full items-center justify-center items-stretch mx-auto mx-8 max-w-7xl'):
            with ui.card().classes('w-full sm:w-1/3 lg:w-1/5 flex-grow p-4'):
                with ui.row().classes('items-center w-full -mt-2'):
                    ui.label('与枫同奔 Run With Fun').classes('text-lg text-bold')
                    ui.chip('词曲').classes('text-xs').props('floating')
                    ui.space()
                    ui.button(icon='open_in_new', on_click=lambda: (ui.navigate.to('https://music.163.com/#/song?id=2148944359'))).props('flat fab-mini')
                ui.label('我愿如流星赶月那样飞奔').classes('text-sm -mt-3')
            with ui.card().classes('w-full sm:w-1/3 lg:w-1/5 flex-grow p-4'):
                with ui.row().classes('items-center w-full -mt-2'):
                    ui.label('HeyFun\'s Story').classes('text-lg text-bold')
                    ui.chip('自设印象曲').classes('text-xs').props('floating')
                    ui.space()
                    ui.button(icon='open_in_new', on_click=lambda: (ui.navigate.to('https://music.163.com/#/song?id=1889436124'))).props('flat fab-mini')
                ui.label('飞奔在星辰大海之间的少年').classes('text-sm -mt-3')
            with ui.card().classes('w-full sm:w-1/3 lg:w-1/5 flex-grow p-4'):
                with ui.row().classes('items-center w-full -mt-2'):
                    ui.label('2020Fall').classes('text-lg text-bold')
                    ui.chip('年度纯音乐').classes('text-xs').props('floating')
                    ui.space()
                    ui.button(icon='open_in_new', on_click=lambda: (ui.navigate.to('https://music.163.com/#/song?id=1863630345'))).props('flat fab-mini')
                ui.label('耗时6个月完成的年度纯音乐').classes('text-sm -mt-3')

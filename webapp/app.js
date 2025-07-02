const EMOJIS = ['😀', '😂', '🤣', '😍', '🥰', '😎', '🤩', '🥳', '🤯', '👻', 
          '💩', '🤖', '👽', '🐶', '🐱', '🦄', '🐉', '🍕', '🍔', '🎮']

const COLOR = ['🔴', '🔵', '🟢', '🟡',
         '🟠', '🟣', '⚫', '⚪']

const output = document.getElementById('output')

function show_info() {
    output.innerHTML() = `<b>info</b>Привет,\n"\
                    "\n"\
                    "Я умею генерировать рандомные эмодзи\n"\
                    "\n"\
                    "Выберите действие из меню ниже.`
}

function show_help() {
    output.innerHTML = `<b>help</b>Доступные команды:
/start - Начать работу
/register - Начать регистрацию
/help - Помощь
/info - Информация
/color - Случайный цвет
/emoji - Случайные эмодзи
/clear - Очистить чат`
}

function random_number() {
    const n = Math.floor(Math.random() * 9) + 1
    output.innerHTML = `<b>rundom number</b>${n}`
}

function random_color() {
    const c = COLOR[Math.floor(Math.random)() * COLOR.length]
    output.innerHTML = `<b>rundom color</b>${c}`
}

function random_emoji() {
    const e = EMOJIS[Math.floor(Math.random)() * EMOJIS.length]
    output.innerHTML = `<b>rundom color</b>${e}`
}

function reroll_dice() {
    const d = Math.floor(Math.random() * 6) + 1
    output.innerHTML = `<b>rundom number</b>${d}`
}

document.getElementById('infobtn').onclick = show_info
document.getElementById('helpbtn').onclick = show_help
document.getElementById('rnumberbtn').onclick = random_number
document.getElementById('rcolorbtn').onclick = random_color
document.getElementById('remojibtn').onclick = random_emoji
document.getElementById('dicebtn').onclick = reroll_dice
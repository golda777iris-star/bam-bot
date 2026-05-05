import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F

BOT_TOKEN = "8776499164:AAGFwSa99fe_dpVkdIx66s1QsN_W8vbRmM0"
ADMIN_ID = 5778248544
CURRENCY = "bam*"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

users = {}
jackpot = {"amount": 10000}

def get_user(uid):
    if uid not in users:
        users[uid] = {"balance": 1000, "games": 0, "wins": 0}
    return users[uid]

def main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Игры", callback_data="games")],
        [InlineKeyboardButton(text="💰 Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="⚙️ Админ", callback_data="admin")]
    ])

@dp.message(Command("start"))
async def start(msg: Message):
    get_user(msg.from_user.id)
    await msg.answer(f"🎮 <b>Bam* Game Bot</b>\n\n💰 Баланс: {users[msg.from_user.id]['balance']} {CURRENCY}", reply_markup=main_kb(), parse_mode="HTML")

@dp.callback_query(F.data == "profile")
async def profile(cb: CallbackQuery):
    u = users[cb.from_user.id]
    await cb.message.edit_text(f"👤 Профиль\n💰 Баланс: {u['balance']} {CURRENCY}\n🎮 Игр: {u['games']}\n🏆 Выиграно: {u['wins']}", reply_markup=main_kb())

@dp.callback_query(F.data == "games")
async def games(cb: CallbackQuery):
    await cb.message.edit_text("🎰 Выбери игру:", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Рулетка", callback_data="roulette")],
        [InlineKeyboardButton(text="💣 Мины", callback_data="mines")],
        [InlineKeyboardButton(text="🎲 Кости", callback_data="dice")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]))

@dp.callback_query(F.data == "roulette")
async def roulette(cb: CallbackQuery):
    await cb.message.edit_text("🎰 Рулетка\nСтавка: 100", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔴 Red", callback_data="r_red"),
         InlineKeyboardButton(text="⚫ Black", callback_data="r_black")],
        [InlineKeyboardButton(text="🔙", callback_data="games")]
    ]))

@dp.callback_query(F.data.startswith("r_"))
async def play_roulette(cb: CallbackQuery):
    uid = cb.from_user.id
    choice = cb.data.split("_")[1]
    bet = 100
    u = users[uid]
    
    if u["balance"] < bet:
        await cb.answer("❌ Недостаточно!", show_alert=True)
        return
    
    u["balance"] -= bet
    result = "red" if choice == "red" else "black"
    win = bet * 2 if choice == result else 0
    
    u["balance"] += win
    u["games"] += 1
    if win > bet:
        u["wins"] += win - bet
    
    emoji = "🔴" if result == "red" else "⚫"
    await cb.message.edit_text(f"🎰 Рулетка\nВыпало: {emoji} {result}\n\n{'✅ ВЫИГРЫШ!' if win > 0 else '❌ ПРОИГРЫШ'}\n+{win} {CURRENCY}\nБаланс: {u['balance']}", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙", callback_data="games")]]))

@dp.callback_query(F.data == "mines")
async def mines(cb: CallbackQuery):
    await cb.message.edit_text("💣 Мины\nСтавка: 100", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 💣", callback_data="mines_1"),
         InlineKeyboardButton(text="3 💣", callback_data="mines_3")],
        [InlineKeyboardButton(text="🔙", callback_data="games")]
    ]))

@dp.callback_query(F.data.startswith("mines_"))
async def play_mines(cb: CallbackQuery):
    uid = cb.from_user.id
    mines_c = int(cb.data.split("_")[1])
    bet = 100
    u = users[uid]
    
    if u["balance"] < bet:
        await cb.answer("❌ Недостаточно!", show…

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from database.db import save_deal, get_history, get_stats

router = Router()

class CalcState(StatesGroup):
    buy = State()
    sell = State()
    invest = State()
    commission = State()

@router.message(Command("start"))
async def start(message: Message):
    text = (
        "🚗 <b>GTA5RP Перекуп Калькулятор</b>\n\n"
        "Команды:\n"
        "/calc — новый расчет\n"
        "/history — история\n"
        "/stats — статистика\n"
        "/help — помощь"
    )

    await message.answer(text)

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "Введите данные сделки, и бот посчитает прибыль."
    )

@router.message(Command("calc"))
async def calc_start(message: Message, state: FSMContext):
    await state.set_state(CalcState.buy)

    await message.answer("💸 Введите цену покупки:")

@router.message(CalcState.buy)
async def calc_buy(message: Message, state: FSMContext):
    await state.update_data(buy=int(message.text))
    await state.set_state(CalcState.sell)

    await message.answer("💰 Введите цену продажи:")

@router.message(CalcState.sell)
async def calc_sell(message: Message, state: FSMContext):
    await state.update_data(sell=int(message.text))
    await state.set_state(CalcState.invest)

    await message.answer("🔧 Вложения:")

@router.message(CalcState.invest)
async def calc_invest(message: Message, state: FSMContext):
    await state.update_data(invest=int(message.text))
    await state.set_state(CalcState.commission)

    await message.answer("📉 Комиссия (%):")

@router.message(CalcState.commission)
async def calc_commission(message: Message, state: FSMContext):
    data = await state.get_data()

    buy = data["buy"]
    sell = data["sell"]
    invest = data["invest"]
    commission = float(message.text)

    fee = sell * (commission / 100)

    profit = sell - buy - invest - fee

    roi = (profit / buy) * 100

    result = (
        "🚗 <b>Результат сделки</b>\n\n"
        f"💸 Покупка: {buy:,}\n"
        f"💰 Продажа: {sell:,}\n"
        f"🔧 Вложения: {invest:,}\n"
        f"📉 Комиссия: {commission}%\n\n"
        f"✅ Чистая прибыль: {profit:,.0f}\n"
        f"📈 ROI: {roi:.2f}%"
    )

    await save_deal(
        message.from_user.id,
        buy,
        sell,
        invest,
        commission,
        profit,
        roi
    )

    await message.answer(result)

    await state.clear()

@router.message(Command("history"))
async def history(message: Message):
    rows = await get_history(message.from_user.id)

    if not rows:
        await message.answer("История пуста")
        return

    text = "📚 Последние сделки\n\n"

    for i, row in enumerate(rows, start=1):
        buy, sell, profit = row

        text += (
            f"{i}. "
            f"Покупка: {buy:,} | "
            f"Продажа: {sell:,} | "
            f"Профит: {profit:,.0f}\n"
        )

    await message.answer(text)

@router.message(Command("stats"))
async def stats(message: Message):
    count, total_profit = await get_stats(message.from_user.id)

    text = (
        "📊 Статистика\n\n"
        f"Сделок: {count}\n"
        f"Общая прибыль: {total_profit:,.0f}"
    )

    await message.answer(text)
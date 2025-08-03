from math import trunc
from dataclasses import dataclass
from tkinter import ttk

@dataclass
class PseudoInput:
    value: str

    def get(self) -> str:
        return self.value

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def calculate_rate(
    window,
    profit_margin,
    usdt_quantity,
    price_currency_from,
    fee_currency_from,
    price_currency_to,
    fee_currency_to,
    result,
    decimal_limit:int = 5
) -> None:        
    profit_value = profit_margin.get()
    usdt_quantity_value = usdt_quantity.get()
    price_currency_from_value = price_currency_from.get()
    fee_currency_from_value = fee_currency_from.get()
    price_currency_to_value = price_currency_to.get()
    fee_currency_to_value = fee_currency_to.get()

    input_values = [
        profit_value,
        usdt_quantity_value,
        price_currency_from_value,
        fee_currency_from_value,
        price_currency_to_value,
        fee_currency_to_value
    ]

    if not all(input_values):
        result.config(
            text="Por favor rellene todos los campos",
            font=("Arial", 12, "italic"),
        )
        return
    if not all(list(map(is_float, input_values))):
        result.config(
            text="solo es posible rellenar los campos con numeros",
            font=("Arial", 12, "italic"),
        )
    else:
        result.config(
            text="solo es posible rellenar los campos con numeros",
            font=("Arial", 36, "bold")
        )
        # compro <usdt_quantity> USDT en la moneda de origen
        original_sended = float(usdt_quantity_value) * float(price_currency_from_value)
        usdt_sended = float(usdt_quantity_value) - float(fee_currency_from_value)

        # vendo <usdt_quantity> USDT en la moneda de destino
        usdt_avilable_for_sell = usdt_sended - float(fee_currency_to_value)
        recibed_currency_to = usdt_avilable_for_sell * float(price_currency_to_value)

        # calculo de la taza bruta por transaccion
        brute_rate = recibed_currency_to / original_sended

        # calculo de la taza incluyendo margen de ganancia
        sugested_rate =  brute_rate * (1 - (float(profit_value) / 100))

        # obtengo taza truncando decimales
        factor = 10 ** decimal_limit
        truncated_sugested_rate = trunc(sugested_rate * factor) / factor

        print(f"enviaste {original_sended} recibiendo {recibed_currency_to} para una taza de {brute_rate}\nPor lo que con el margen de {profit_value} se recomienda la taza de {truncated_sugested_rate}")
        result.config(text=truncated_sugested_rate)

        window.clipboard_clear()
        window.clipboard_append(truncated_sugested_rate)
        window.update()
        print("✅ texto copiado:", truncated_sugested_rate)

def run_app(window, context):
    window.title("Calculador de Tazas para Remesas")
    ttk.Label(
        window,
        text="Margen de Ganancia por operación"
    ).pack(pady=(10,10))
    profit_margin = ttk.Entry(window) # margen de ganancia en %
    profit_margin.insert(0, "3.5")
    profit_margin.pack(pady=(0, 10))
    usdt_quantity = PseudoInput("10") # USDT referencia para obtener precios de compra y venta

    ttk.Label(
        window,
        text="El precio de comprar 10 USDT en moneda de Origen"
    ).pack(pady=(10, 10))
    price_currency_from = ttk.Entry(window) # precio de COMPRAR USDT en moneda de origen
    price_currency_from.pack(pady=(0, 10))

    fee_currency_from = PseudoInput("0.05") # fee pagado en USDT por comprar

    ttk.Label(
        window,
        text="El precio de vender 10 USDT en moneda de Destino"
    ).pack(pady=(10,10))

    price_currency_to = ttk.Entry(window) # precio de VENDER USDT en moneda de origen
    price_currency_to.pack(pady=(0, 10))
    fee_currency_to = PseudoInput("0.05") # fee pagado en USDT por vender

    result = ttk.Label(
        window,
        text="",
    )

    button = ttk.Button(
        window, text="Calcular y Copiar", command=lambda:calculate_rate(
            window=window,
            result=result,
            usdt_quantity=usdt_quantity,
            profit_margin=profit_margin,
            price_currency_from=price_currency_from,
            fee_currency_from=fee_currency_from,
            price_currency_to=price_currency_to,
            fee_currency_to=fee_currency_to
        )
    )
    button.pack(pady=10)
    result.pack(pady=(10,10))

import gradio as gr
import matplotlib.pyplot as plt
import numpy as np

class Product:
    def __init__(self, name, fixed_costs, variable_costs_per_subscription, price_per_subscription, profit_margin):
        self.name = name
        self.fixed_costs = fixed_costs
        self.variable_costs_per_subscription = variable_costs_per_subscription
        self.price_per_subscription = price_per_subscription
        self.profit_margin = profit_margin

    def calculate_break_even_point(self):
        if self.price_per_subscription <= self.variable_costs_per_subscription:
            return {
                "kg": f"Өзүн-өзү актоо чекити {self.name} үчүн эсептелбейт, анткени жазылуу баасы бир жазылуу үчүн өзгөрмөлүү чыгымдарга барабар же андан төмөн.",
                "ru": f"Точка безубыточности для {self.name} не может быть рассчитана, так как цена за подписку меньше или равна переменным затратам за подписку."
            }
        break_even_point = self.fixed_costs / (self.price_per_subscription - self.variable_costs_per_subscription)
        return {
            "kg": f"Өзүн-өзү актоо үчүн {self.name} жазылууларынын {break_even_point:.2f} сатууңуз керек.",
            "ru": f"Вам нужно продать {break_even_point:.2f} подписок на {self.name}, чтобы выйти на точку безубыточности."
        }

    def suggested_price(self):
        suggested_price = self.variable_costs_per_subscription * (1 + self.profit_margin / 100)
        return {
            "kg": f"{self.name} үчүн сунушталган баа {self.profit_margin}% пайда маржасын камсыз кылуу үчүн ${suggested_price:.2f}.",
            "ru": f"Рекомендуемая цена для {self.name} составляет ${suggested_price:.2f} для обеспечения маржи прибыли в {self.profit_margin}%."
        }

class EducationalCenter:
    def __init__(self):
        self.products = []

    def add_product(self, name, fixed_costs, variable_costs_per_subscription, price_per_subscription, profit_margin):
        product = Product(name, fixed_costs, variable_costs_per_subscription, price_per_subscription, profit_margin)
        self.products.append(product)

    def calculate_break_even_points(self):
        results = []
        suggestions = []
        for product in self.products:
            results.append(product.calculate_break_even_point())
            suggestions.append(product.suggested_price())
        return results, suggestions

def format_results(results, suggestions):
    kg_results = "\n".join([res["kg"] for res in results])
    ru_results = "\n".join([res["ru"] for res in results])
    kg_suggestions = "\n".join([sug["kg"] for sug in suggestions])
    ru_suggestions = "\n".join([sug["ru"] for sug in suggestions])
    return kg_results, ru_results, kg_suggestions, ru_suggestions

def plot_graph(names, fixed_costs, variable_costs, prices, profit_margin):
    fig, ax = plt.subplots()

    for name, fixed_cost, variable_cost, price in zip(names, fixed_costs, variable_costs, prices):
        if price > variable_cost:
            break_even_point = fixed_cost / (price - variable_cost)
            suggested_price = variable_cost * (1 + profit_margin / 100)
            x = np.linspace(0, break_even_point * 1.5, 100)
            total_cost = fixed_cost + variable_cost * x
            revenue = price * x

            ax.plot(x, total_cost, label=f'Total Cost ({name})')
            ax.plot(x, revenue, label=f'Revenue ({name})')
            ax.axvline(break_even_point, color='r', linestyle='--', label=f'Break-Even Point ({name})')
            ax.axhline(fixed_cost, color='g', linestyle='--', label=f'Fixed Cost ({name})')
            ax.scatter(break_even_point, fixed_cost + variable_cost * break_even_point, color='black')
            ax.text(break_even_point, fixed_cost + variable_cost * break_even_point, f'  BEP ({name})')

    ax.set_xlabel('Number of Subscriptions')
    ax.set_ylabel('Cost/Revenue')
    ax.legend()
    ax.set_title('Break-Even Analysis')
    plt.close(fig)
    return fig

def calculate_bep(names, fixed_costs, variable_costs, prices, profit_margin):
    try:
        names = [name.strip() for name in names.split(',')]
        fixed_costs = [float(cost.strip()) for cost in fixed_costs.split(',')]
        variable_costs = [float(cost.strip()) for cost in variable_costs.split(',')]
        prices = [float(price.strip()) for price in prices.split(',')]
        
        if not (len(names) == len(fixed_costs) == len(variable_costs) == len(prices)):
            return ("Бардык киргизүүлөр бирдей санда болушун текшериңиз.", 
                    "Пожалуйста, убедитесь, что все входные данные имеют одинаковое количество записей.",
                    None)
        
        educational_center = EducationalCenter()
        
        for name, fixed_cost, variable_cost, price in zip(names, fixed_costs, variable_costs, prices):
            educational_center.add_product(name, fixed_cost, variable_cost, price, profit_margin)
        
        results, suggestions = educational_center.calculate_break_even_points()
        kg_results, ru_results, kg_suggestions, ru_suggestions = format_results(results, suggestions)
        fig = plot_graph(names, fixed_costs, variable_costs, prices, profit_margin)
        return kg_results, ru_results, kg_suggestions, ru_suggestions, fig

    except ValueError:
        return ("Чыгымдар жана баалар үчүн жарактуу сандык маанилерди киргизиңиз.", 
                "Пожалуйста, введите допустимые числовые значения для затрат и цен.",
                None)


# Вставка логотипа выше всего интерфейса
title = "Пайда маржасы боюнча сунуштар менен өзүн-өзү актоо чекити калькулятору / Калькулятор точки безубыточности с предложениями по марже прибыли"
description = "Бир нече продукт үчүн өзүн-өзү актоо чекитин эсептеңиз жана туруктуу чыгымдарга, бир жазылуу үчүн өзгөрмөлүү чыгымдарга, жазылуу баасына жана каалаган пайда маржасына негизделген жакшыраак баалар боюнча сунуштарды алыңыз. / Рассчитайте точки безубыточности для нескольких продуктов и получите предложения по более выгодным ценам на основе постоянных затрат, переменных затрат на подписку, цены за подписку и желаемой маржи прибыли."

iface = gr.Interface(
    fn=calculate_bep,
    inputs=[
        gr.Textbox(label="Продукт аттары (вергүл менен бөлүнгөн) / Названия продуктов (через запятую)"),
        gr.Textbox(label="Жалпы туруктуу чыгымдар доллар менен (вергүл менен бөлүнгөн) / Общие постоянные затраты в долларах (через запятую)"),
        gr.Textbox(label="Жазылуу үчүн өзгөрмөлүү чыгымдар доллар менен (вергүл менен бөлүнгөн) / Переменные затраты на подписку в долларах (через запятую)"),
        gr.Textbox(label="Бир бирдигинин баасы доллар менен (вергүл менен бөлүнгөн) / Цена за единицу в долларах (через запятую)"),
        gr.Slider(0, 100, step=1, label="Каалаган пайда маржасы (%) / Желаемая маржа прибыли (%)")
    ],
    outputs=["text", "text", "text", "text", gr.Plot()],
    title=title,
    description=description,
    theme="dark"
)

iface.launch(share=True)

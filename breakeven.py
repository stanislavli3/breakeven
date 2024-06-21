import gradio as gr

class EducationalCenter:
    def __init__(self, fixed_costs, variable_costs_per_subscription, price_per_subscription):
        self.fixed_costs = fixed_costs
        self.variable_costs_per_subscription = variable_costs_per_subscription
        self.price_per_subscription = price_per_subscription

    def calculate_break_even_point(self):
        # Calculate break-even point
        if self.price_per_subscription <= self.variable_costs_per_subscription:
            return "Break-even point cannot be calculated as the price per subscription is less than or equal to the variable costs per subscription."
        break_even_point = self.fixed_costs / (self.price_per_subscription - self.variable_costs_per_subscription)
        return break_even_point

def calculate_bep(fixed_costs, variable_costs, price):
    try:
        # Convert inputs to float
        fixed_costs = float(fixed_costs)
        variable_costs = float(variable_costs)
        price = float(price)
        
        # Create EducationalCenter instance
        educational_center = EducationalCenter(fixed_costs, variable_costs, price)
        
        # Calculate break-even point
        break_even_point = educational_center.calculate_break_even_point()
        
        if isinstance(break_even_point, str):
            return break_even_point
        else:
            return f"The break-even point is {break_even_point:.2f} subscriptions."
    except ValueError:
        return "Please enter valid numerical values for costs and prices."

# Create Gradio interface
iface = gr.Interface(
    fn=calculate_bep,
    inputs=[
        gr.Textbox(label="Total Fixed Costs in dollars"),
        gr.Textbox(label="Variable Cost per Subscription in dollars"),
        gr.Textbox(label="Price per Subscription in dollars")
    ],
    outputs="text",
    title="Break-Even Point Calculator",
    description="Calculate the break-even point for an educational center based on fixed costs, variable costs per subscription, and price per subscription."
)

# Launch the interface
iface.launch()

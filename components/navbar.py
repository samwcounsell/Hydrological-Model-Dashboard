import dash_bootstrap_components as dbc


# Creating the navbar for the top of every page within the app
def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                children=[
                    dbc.DropdownMenuItem("Home", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Plots", href='/plots'),
                    dbc.DropdownMenuItem("PlotsB", href='/plotsb'),
                    dbc.DropdownMenuItem("About", href='/about')
                ],
            ),
        ],
        brand="Water Resources Dashboard",
        brand_href="/home",
        sticky="top",
        color="lightseagreen",
        dark=True
    )

    return navbar

import plotly.graph_objects as go


def create_dna_radar(dna):

    categories = [
        "Growth",
        "Value",
        "Stability",
        "Momentum",
        "Risk",
    ]

    values = [
        dna["Growth"],
        dna["Value"],
        dna["Stability"],
        dna["Momentum"],
        dna["Risk"],
    ]

    # close polygon
    categories += [categories[0]]
    values += [values[0]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name="DNA",
            line=dict(
                color="#22C55E",
                width=4,
            ),
            fillcolor="rgba(34,197,94,0.18)",

            marker=dict(
                size=8,
                color="#22C55E",
            ),
                    )
                )

    fig.update_layout(

        polar=dict(

            bgcolor="rgba(0,0,0,0)",

            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#9CA3AF"),
                gridcolor="#273449",
                linecolor="#273449",
            ),

            angularaxis=dict(
                tickfont=dict(
                    color="white",
                    size=12,
                ),
                gridcolor="#273449",
                linecolor="#273449",
            ),
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10,
        ),

        showlegend=False,

        height=330,
    )

    return fig
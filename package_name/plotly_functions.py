# plotting tools
import plotly
import plotly.express as px
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.graph_objects as go
class DataPlot():
    """ Takes in the dataframe that should be used in the plotting. Has built in
        plotting functions for different plotting dataframe series. 
    """
    def __init__(self, df=pd.DataFrame(), display_plot=False, title = None):
        """ Init function is defining figure parmaters
            - df The dataframe were the values tombe plotted is stored
            - display_plot- if True, all plots are displayed
            - Title to displayed in figures- defaulted to number of datapoints
        """
        self.df = df
        self.display_plot = display_plot
        self.title = title
        if title == None: 
            self.title  = 'Number of datapoints: '+str(self.df.shape[0])
    def fast(self,y_var: str):
        """ Plots a single time series. 
        """
        fig = go.Figure()
        fig.add_trace(go.Scattergl(x=self.df.index, y=self.df[y_var], mode='markers', name=y_var))
        fig.update_layout(
                        title=self.title,
        )
        if self.display_plot:
            fig.show()
        return fig
    def plot(self, x_var: str, y_var: str):
        """ Plots a single y-variable against a single x-variable and returns a 
            figure
        """
        fig = go.Figure()
        fig.add_trace(go.Scattergl(x=self.df[x_var], y=self.df[y_var], mode='markers', name=y_var))
        fig.update_layout(
                        title=self.title,
                xaxis_title=x_var,
                yaxis_title=y_var,

        )
        if self.display_plot:
            fig.show()
        return fig
    def plot_color(self, x_var:str , y_var: str, color: str):
        """ Plots two variables against each other with a third variable as color
        """
        fig = go.Figure()
        fig.add_trace(go.Scattergl(x=self.df[x_var], y=self.df[y_var], mode='markers', 
        marker=dict(
        size=6,
        color=self.df[color],
        colorbar=dict(
            title=color,
            lenmode='fraction',
            len=0.75        ),
        colorscale="Viridis"
        ),
        text=self.df[color],
        hovertemplate =  'Y Value: %{y:.2f}'+
                        '<br>X Value: %{x}<br>'+
                        'Color Value: %{text:.2f}<extra></extra>',
        name=y_var))

        fig.update_layout(
                        title=self.title,
                xaxis_title=x_var,
                yaxis_title=y_var,

        )
        if self.display_plot:
            fig.show()
        
        return fig

    def hist(self, x_var: str, show_statistical_data:bool = False):
        """ Plots a histogram of the input variable
        """
        fig = go.Figure()
        fig.add_trace(go.Histogram(x = self.df[x_var]))
        fig.update_layout(title=self.title,
                        xaxis_title=x_var,
                        yaxis_title='Count',
                            )
        if show_statistical_data:
            text = self.df[x_var].describe()
            hist_text = ''
            for index, value in text.items():
                hist_text +=(f"{index}: {value:.4} <br>")
            fig.update_layout(
            annotations=[
            go.layout.Annotation(
                text=f'{hist_text}',
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.0,
                y=1.0,
                bordercolor='red',
                borderwidth=1
            )
        ]
    )
        if self.display_plot:
            fig.show()
        return fig

    def fast_multiple(self,y_var:str):
        """ Makes a timeline plot with multiple y variables based on the index of
            the dataframe. 
        """
        fig = go.Figure()
        for y_tag in y_var:
            fig.add_trace(go.Scattergl(x=self.df.index, y=self.df[y_tag], mode='markers', name=y_tag))
        fig.update_layout(
                        title=self.title,
        )
        if self.display_plot:
            fig.show()
        return fig
    
    def comparison(self, x_var: str, y_var: list):
        """ Plot for comparing multiple vy variables against a single x-variable
            Each of the yn variables are plotted agains
        """
        fig = go.Figure()
        for y_tag in y_var:
            fig.add_trace(go.Scattergl(
                x=self.df[x_var],
                y=self.df[y_tag],
                marker=dict(size=6),
                mode="markers",
                name=y_tag,
            ))

        fig.update_layout(
                        title=self.title,
                yaxis_title= y_var[0],
                xaxis_title=x_var,

        )
        if self.display_plot:
            fig.show()
        return fig
    
    def plot_multiple(self, x_vars: list, y_var: list, legend=False):
        """ Takes in multiple tags for x and y variables and plots them together in a scatterplot. The axis are represneted 
            by the first values of the tag
        """
        fig = go.Figure()
        if legend == False: legend = y_var
        for index, y_tag in enumerate(y_var):
            fig.add_trace(go.Scattergl(x=self.df[x_vars[index]], y=self.df[y_tag], mode='markers', name=legend[index]))
        fig.update_layout(
                        title=self.title,
                        xaxis_title=x_vars[0],
                        yaxis_title=y_var[0],

        )
        if self.display_plot:
            fig.show()
        return fig
    
    def save_html_plots(self, fig_list, file_name):
        """ Takes in the figures in fig_list and saves them in an html file with name
            file_name.
        """
        with open(file_name+'.html', 'w') as f:
            for fig in fig_list:
                f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        pass
    def hist_divided(self, var, show_statistical_data:bool =False, category: str = None):
        """ Plots a histogram of the input variable, where the the histogram is 
            divided by traces into different categories defined by category 
            column. Category columns must have limited number of unique values. 
            If show_statistical_data is set to True then a small box with statisitcal
            metrics is displayed. 
        """
        fig = go.Figure()
        if category is not None:
            fig.add_trace(go.Histogram(x = self.df[var], name='All values'))
            for unique_value in self.df[category].unique():
                fig.add_trace(go.Histogram(x = self.df.loc[self.df[category] == unique_value, var], name = category+': '+str(unique_value)))
        else:
            fig.add_trace(go.Histogram(x = self.df[var]))
        fig.update_layout(
                        title = self.title,
                        xaxis_title=var,
                        yaxis_title='Count',
                            )
        if show_statistical_data:
            text = self.df[var].describe()
            hist_text = '<b>Data All Values: </b> <br>'
            for index, value in text.items():
                hist_text +=(f"{index}: {value:.4} <br>")
            fig.update_layout(
            annotations=[
            go.layout.Annotation(
                text=f'{hist_text}',
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.0,
                y=1.0,
                bordercolor='red',
                borderwidth=1)])
        return fig

    def add_plot(self, fig: go.Figure(), x_var: str, y_var: str, add_axis: bool = False):
        """ Takes in a figre value and add a single x-variable and y-variable to 
            it. The add_axis input value decides if the new value should have 
            a secondary axis.
        """
        fig.add_trace(go.Scattergl(x=self.df[x_var], y=self.df[y_var], mode='markers', name=y_var, yaxis="y2"))
        if add_axis:
            fig.update_layout(
                yaxis2=dict(
                title=y_var,
                titlefont=dict(
                    color="#d62728"
                ),
                tickfont=dict(
                    color="#d62728"
                ),
                anchor="x",
                overlaying="y",
                side="right"
            ),)

        if self.display_plot:
            fig.show()
        return fig
        
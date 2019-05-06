import quandl
import pandas as pd
from bokeh.models import ColumnDataSource
from flask import Flask, render_template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)


@app.route('/plotone')
def bokeh():


    co2_emissions_all=pd.read_csv('Total_carbon_dioxide_emissions_from_all_sectors_all_fuels_United_States.csv',index_col=False)
    co2_emissions_all.index=(pd.date_range(start='1980-01-01', periods=len(co2_emissions_all), freq='A'))[::-1]
    co2_emissions_all.sort_index(inplace=True)
    co2_emissions_all.drop(['Year'], axis=1,inplace=True)
    co2_emissions_all.index.name='Year'
    co2_emissions_all=co2_emissions_all[co2_emissions_all.index>'1990-01-01']
    co2_emissions_all=co2_emissions_all.rename(columns = {'Series ID: EMISS.CO2-TOTV-TT-TO-US.A million metric tons CO2':'co2_all'})
    #(co2_emissions_all['co2_all']/co2_emissions_all['co2_all'][0]).plot();

    co2_emissions_ng=pd.read_csv('Total_carbon_dioxide_emissions_from_all_sectors_natural_gas_United_States.csv',index_col=False)
    co2_emissions_ng.index=(pd.date_range(start='1980-01-01', periods=len(co2_emissions_ng), freq='A'))[::-1]
    co2_emissions_ng.sort_index(inplace=True)
    co2_emissions_ng.drop(['Year'], axis=1,inplace=True)
    co2_emissions_ng.index.name='Year'
    co2_emissions_ng=co2_emissions_ng[co2_emissions_ng.index>'1990-01-01']
    co2_emissions_ng=co2_emissions_ng.rename(columns = {'Series ID: EMISS.CO2-TOTV-TT-NG-US.A million metric tons CO2':'co2_Ngas'})
    #(co2_emissions_ng['co2_Ngas']/co2_emissions_ng['co2_Ngas'][0]).plot();

    co2_emissions_oil=pd.read_csv('Total_carbon_dioxide_emissions_from_all_sectors_petroleum_United_States.csv',index_col=False)
    co2_emissions_oil.index=(pd.date_range(start='1980-01-01', periods=len(co2_emissions_oil), freq='A'))[::-1]
    co2_emissions_oil.sort_index(inplace=True)
    co2_emissions_oil.drop(['Year'], axis=1,inplace=True)
    co2_emissions_oil.index.name='Year'
    co2_emissions_oil=co2_emissions_oil[co2_emissions_oil.index>'1990-01-01']
    co2_emissions_oil=co2_emissions_oil.rename(columns = {'Series ID: EMISS.CO2-TOTV-TT-PE-US.A million metric tons CO2':'co2_oil'})
    #(co2_emissions_oil['co2_oil']/co2_emissions_oil['co2_oil'][0]).plot();

    plot_8_data=pd.concat([co2_emissions_oil.co2_oil/co2_emissions_oil.co2_oil[0],co2_emissions_ng.co2_Ngas/co2_emissions_ng.co2_Ngas[0],\
            co2_emissions_all.co2_all/co2_emissions_all.co2_all[0],],axis=1)#.plot(figsize=(16,9))
    
    plot_8_data.index.name='Month'
    source=ColumnDataSource(plot_8_data)
    p = figure(title='normalized co2_emissions', plot_width=600, plot_height=600, x_axis_type="datetime")

    p.xaxis.axis_label = "Months**"
    p.yaxis.axis_label = "petroleum_co2+gas_co2+all_co2"
    p.line(x='Month', y='co2_oil', line_width=2, source=source, color="black",legend='petroleum_co2_emis+')
    p.line(x='Month', y='co2_Ngas', line_width=2, source=source,color="green" ,legend='gas_co2_emis+')
    p.line(x='Month', y='co2_all', line_width=2, source=source, color="navy",legend='all_co2_emis+')

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    
    # render template
    script, div = components(p)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)

if __name__ == '__main__':
    app.run(debug=True)



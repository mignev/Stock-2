import React from 'react';
import {
    ScatterChart, Scatter, XAxis, YAxis, Tooltip, Legend, CartesianGrid, Label
} from 'recharts';
import ChartContainer from '../chartContainer/chartContainer'

const scatterPlot = ({ title, tooltip, data1, data2, data3, loading, blur }) => {
    return (
        <ChartContainer tooltip={tooltip} title={title} blur={blur} loading={loading} placeholder="Select 2+ companies">
            <ScatterChart
                margin={{
                    top: 20, right: 20, left: 5, bottom: 20,
                }}
            >
                <Scatter data={data1} fill="#8884d8" name="Return/Volatility" />
                <Scatter data={data2} fill="#090909" name="Max Sharpe Ratio" shape="star" />
                <Scatter data={data3} fill="#D7263D" name="Min Volatility" shape="triangle" />
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" dataKey="volatility" name="Expected Volatility" unit="%" domain={['auto', 'auto']}>
                    <Label value="Expected Volatility" position="insideBottomRight" offset={-7} />
                </XAxis>
                <YAxis type="number" dataKey="returns" name="Expected Returns" unit="%" domain={['auto', 'auto']}
                // label={{ value: 'Expected Returns', angle: -90, position: 'left' }}
                />
                <Tooltip />
                <Legend />
            </ScatterChart>
        </ChartContainer>
    );
}

export default scatterPlot

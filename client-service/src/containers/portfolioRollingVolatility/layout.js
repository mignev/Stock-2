import React from 'react'
import logic from './logic'
import LineChart from '../charts/lineChart/lineChart'


const Layout = () => {
    const { stocks, rollingVolatility, loading } = logic()
    return (
        <LineChart
            placeholder='Select 2+ Companies'
            blur={stocks.length < 2}
            title='Portfolio Volatility'
            tooltip='Volatility of portfolio every 6 months'
            data={rollingVolatility}
            stocks={['equal', 'optimal', 'minimal']}
            dataKey="date"
            loading={loading}
        ></LineChart>
    )
}

export default Layout

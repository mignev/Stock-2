import React, { useEffect } from 'react'
import { fetchStockPriceChange } from '../../redux/actions'
import { useSelector, useDispatch, shallowEqual } from 'react-redux'


const Logic = () => {
    const stocks = useSelector(state => state.stockReducer.symbolList);
    const stockPriceChange = useSelector(state => state.stockReducer.stockPriceChange);

    return { stockPriceChange, stocks }
}

export default Logic

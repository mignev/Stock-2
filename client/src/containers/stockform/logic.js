import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getMetrics } from '../../redux/actions'
import stocks from './stocksList'


const Logic = () => {
    const [state, setState] = useState({
        symbol: {},
        stocks: stocks
    });
    const dispatch = useDispatch();
    const symbols = useSelector(state => state.stockReducer.symbolList)
    const initialSymbols = useSelector(state => state.stockReducer.initialSymbols)

    const handleChange = symbol => {
        setState({ ...state, symbol });
    };

    const handleClick = (e) => {
        e.preventDefault()
        if (!symbols.includes(state.symbol.symbol)) {
            const payload = [...symbols, state.symbol.symbol]
            dispatch(getMetrics(payload))
            setState({ ...state, symbol: {} })
        }
    }

    const handleInitialState = () => {
        const missing = []
        if (!symbols.includes(initialSymbols[0]))
            missing.push(initialSymbols[0])
        if (!symbols.includes(initialSymbols[1]))
            missing.push(initialSymbols[1])
        if (missing.length > 0) dispatch(getMetrics(missing))
        else return;
    }

    useEffect(() => {
        handleInitialState()
    }, [])

    return { state, handleChange, handleClick }
}

export default Logic





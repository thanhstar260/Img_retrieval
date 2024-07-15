import React, { useState } from 'react'
import { twMerge } from 'tailwind-merge';

const BrushSizeSlider = ({value, onChange, className}) => {
    const MAX = 48;
    const getBackgroundSize = (() => {
        return {backgroundSize: `${(value * 100 / MAX)}% 100%`}
    })

  return (
    <div className={
        twMerge('flex items-center',
            className
        )
    }>
        <input 
            type='range' 
            min='1' 
            max={MAX} className='slider h-1.5 rounded-md bg-slate-200 mr-3'
            onChange={onChange}
            style={getBackgroundSize()} value={value}/>
        <input type='number' value={value} className='text-slate-600 number-input focus:outline-none bg-transparent' min={1} max={MAX} onChange={onChange}/>
    </div>
  )
}

export default BrushSizeSlider
import React, { useState } from 'react'
import { twMerge } from 'tailwind-merge'

const OutlineButton = ({className, onClick, isSelected = false, children, ...props}) => {

  return (
    <button 
    className={twMerge(
        'px-3 py-2 rounded-md border-2 border-teal-500 flex justify-center items-center gap-2 hover:bg-teal-500 hover:text-white text-teal-500 transition-all',
        className
    )}
    onClick={onClick}
    {...props}
    >
        {children}
    </button>
  )
}

export default OutlineButton
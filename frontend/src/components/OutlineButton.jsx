import React, { useState } from 'react'
import { twMerge } from 'tailwind-merge'

const OutlineButton = ({className, onClick, isSelected = false, children, ...props}) => {

  return (
    <button 
    className={twMerge(
        'px-3 py-2 rounded-md border border-teal-500',
        `${isSelected ? 'bg-teal-500 text-white' : 'bg-transparent text-teal-500'}`,
        className
    )}
    onClick={onClick}
    >
        {children}
    </button>
  )
}

export default OutlineButton
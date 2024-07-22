import React, { useState } from 'react'
import { twMerge } from 'tailwind-merge'

const IconButton = ({className, onClick, onDoubleClick, isSelected = false, label, children, ...props}) => {

  return (
    <div 
    onClick={onClick}
    onDoubleClick={onDoubleClick}
    className={twMerge(
        'group relative w-fit h-fit px-2 py-2 rounded-full hover:shadow-md cursor-pointer transition-all',
        `${isSelected ? 'bg-teal-500 text-white' : 'bg-transparent text-teal-500'}`,
        className
    ) 
    }
    {...props} >
            {children}
            {label ? <div className='text-center hidden group-hover:block rounded-md p-1 absolute top-[120%] z-10 text-xs bg-slate-800 -translate-x-1/2 left-1/2 shrink-0 min-w-16'>{label}</div> : undefined}
    </div>
  )
}

export default IconButton
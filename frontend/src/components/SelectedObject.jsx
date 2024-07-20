import React from 'react'
import IconButton from './IconButton'
import { IoCloseOutline } from "react-icons/io5";

const SelectedObject = ({name, color, onRemove}) => {
  return (
    <div className='pl-2 pr-8 py-1 rounded-md w-fit text-white relative text-sm' style={{backgroundColor: color}}>
        {name}
        <IconButton 
            className='absolute bottom-1/2 translate-y-1/2 right-0.5 p-1'
            onClick={onRemove} 
            >
            <IoCloseOutline />
        </IconButton>
    </div>
  )
}

export default SelectedObject
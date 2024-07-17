import React, { useCallback, useEffect, useRef, useState } from 'react'
import { twMerge } from 'tailwind-merge';
import { LuChevronsUpDown } from "react-icons/lu";

const SelectMenu = ({className,options, selected, onSelect}) => {

  const [value, setValue] = useState(selected)

  const [filterList, setFilterList] = useState(options);

  const [showItems, setShowItems] = useState(false);
  const selectRef = useRef(null)

  const handleClickSelectMenu = () => {
    setShowItems((prev) => !prev);
  }

  const handleSelectItem = (event, id) => {
    event.stopPropagation();
    onSelect(id);
    setShowItems(false);
    setValue(id);
  }

  const handleClickOutSide = (event) => {
    if(showItems && selectRef.current && !selectRef.current.contains(event.target)) {
      setShowItems(false);
      if(selected !== value) {
        setValue(selected)
      }
    }
  }

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutSide)
    return () => {
      document.removeEventListener('mousedown', handleClickOutSide)
    }
  }, [])

  const handleChangeValue = (event) => {
    const val = event.target.value;
    setValue(val);
    setFilterList(options.filter(elm => {
      return elm.toLowerCase().includes(val.toLowerCase());
    }))
  }

  return (
    <div
      ref={selectRef}
      className={
        twMerge(
          'relative inline-block ring-1 rounded-md py-0.5 px-4 ring-slate-500 min-w-40 text-slate-600 cursor-pointer bg-white',
        className)
    } onClick={handleClickSelectMenu}>
        <input 
          className='max-w-[90%] focus:outline-none ' 
          value={value} onChange={handleChangeValue}/>
        <LuChevronsUpDown className='absolute bottom-1/2 translate-y-1/2 right-3'/>
       {
        showItems &&  <div className='absolute top-[120%] bg-white w-ful left-0 right-0 z-[20] rounded-lg shadow-md overflow-hidden'>
        <ul 
          className=
          ' max-h-48 overflow-y-scroll'>
          {filterList.map(option =>
            <li
            key={option}
            className={
              twMerge(
                'px-4 py-1 hover:bg-teal-500 hover:text-white',
                `${selected === option ? 'text-teal-500' : ''}`
              )
            }
            onClick={(event) => handleSelectItem(event, option)}>
              <span>{option}</span>
            </li>) }
        </ul>
      </div>
       }
    </div>
  )
}

export default SelectMenu
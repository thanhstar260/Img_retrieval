import React, { useState } from 'react'
import IconButton from '../components/IconButton';
import { MdOutlineKeyboardVoice } from "react-icons/md";

const SearchBar = () => {
    let [noResults, setNoResult] = useState(undefined);


  return (
    <div className=' w-80 bg-slate-100 h-screen px-6 py-8'>
        <IconButton 
            label="Speech"
            >
            <MdOutlineKeyboardVoice className=' text-lg' />
        </IconButton>
    </div>
  )
}

export default SearchBar;
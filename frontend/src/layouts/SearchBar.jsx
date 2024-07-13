import React, { useState } from 'react'
import IconButton from '../components/IconButton';
import { MdOutlineKeyboardVoice } from "react-icons/md";
import Stage from '../components/Stage';

const SearchBar = () => {
    let [noResults, setNoResult] = useState(undefined);


  return (
    <div className='w-80 bg-slate-100 h-screen px-6 py-8'>
        <Stage r/>
    </div>
  )
}

export default SearchBar;
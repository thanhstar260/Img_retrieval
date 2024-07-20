import React from 'react'

const LangRadioGroup = ({value, onChange, name}) => {
  return (
    <div className='text-teal-500'>
        <div className='inline-block accent-teal-500 mr-4'>
            <input className='mr-1' type='radio' name={name} value='eng' id='eng' checked={value==="eng"}
            onChange={onChange}/>
            <label htmlFor='eng'>ENG</label>
        </div>
        <div className='inline-block'>
            <input className='accent-teal-500 mr-1'
            type='radio' name={name} value='vie' id='vie' checked={value === "vie"} onChange={onChange}/>
            <label htmlFor='vie'>VIE</label>
        </div>
    </div>
  )
}

export default LangRadioGroup
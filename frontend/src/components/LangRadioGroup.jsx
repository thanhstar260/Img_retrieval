import React from 'react'

const LangRadioGroup = ({value, onChange}) => {
  return (
    <div className='text-teal-500'>
        <div className='inline-block mr-4'>
            <input className='mr-1 accent-teal-500'
            type='radio' name='lang' value='vie' id='vie' checked={value === "vie"} onChange={onChange}/>
            <label htmlFor='vie'>VIE</label>
        </div>
        <div className='inline-block accent-teal-500'>
            <input className='mr-1' type='radio' name='lang' value='eng' id='eng' checked={value==="eng"}
            onChange={onChange}/>
            <label htmlFor='eng'>ENG</label>
        </div>
    </div>
  )
}

export default LangRadioGroup
import React from 'react'

const TextSearchControl = ({id, label, data, onChange}) => {
  console.log("log", data);
  const handleChangeData = (e) => {
    console.log("hello")
    const text = e.target.value;
    onChange(id, text);
  }

  return (
    <div>
        <label className='text-sm text-teal-500 mb-2 inline-block' htmlFor={id}>{label}</label>
        <textarea id={id} rows="4" className="resize-none w-full rounded-lg ring-2 ring-slate-300 focus:outline-none
        focus:ring-teal-500
        px-3
        py-3
        h-auto" 
        value={data || ""}
        onChange={handleChangeData}>
        </textarea>
    </div>
  )
}

export default TextSearchControl
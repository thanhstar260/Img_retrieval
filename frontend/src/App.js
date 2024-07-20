import SearchBar from './layouts/SearchBar';
import { useState } from 'react';
import Result from './layouts/Result';


function App() {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [result, setResult] = useState({})

  const handleSubmit = async (data) => {
    const stages = Object.values(data);
    const stagesBody = [];
    for(let stage of stages) {
      let count = 0
      for(let type in stage.data) {
        console.log(type)
        if(type === 'object')
          continue
        if(stage.data[type]) 
          count++;
        else {
          delete stage.data[type]
        }
      }
      if(count != 1) {
        alert("Each type has to have one type from scene or image, text, speech, sketch")
        return;
      }    
      const type = Object.keys(stage.data)[0];
      const data = stage.data[type];
      const objectInput = stage.data['object']
      let object;
      if(objectInput) {
        object = {}
        let group = Object.groupBy(objectInput, (object) => object.object)
        console.log(object)
        for(let obj in group) {
          const elm = group[obj].map((elm) => elm.offset)
          object[obj] = elm 
        }

      }
      const lang = stage['lang']
      stagesBody.push({type, data, object, lang});

    }

    const body = {stages: stagesBody}
    console.log(body)


    setIsSubmitting(true);
    const response = await fetch("http://127.0.0.1:8000/", {
      headers: {
        'Content-Type': 'application/json',
      },
      method: "POST",
      body: JSON.stringify(body)
    })
    const json = await response.json();
    setResult(json);
    setIsSubmitting(false);
    

}

  return (
    <div className="App flex">
      <SearchBar onSubmit={handleSubmit} isSubmitting={isSubmitting}/>
      <Result />
    </div>
    
  );
}

export default App;

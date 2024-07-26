import SearchBar from "./layouts/SearchBar";
import { useState, useEffect } from "react";
import Result from "./layouts/Result";
import { GoArrowRight } from "react-icons/go";
import IconButton from "./components/IconButton";

function App() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState({});
  const [K, setK] = useState(40);
  const [open, setOpen] = useState(true);
  var dataRerank = null;
  const [resultHistory, setResultHistory] = useState([]);
  const [index, setIndex] = useState(0);
  const [isBack, setIsBack] = useState(false);

  const BacktoResult = ()=>{
    if(index + 1 < resultHistory.length) {
      setResult(resultHistory[index+1])
      setIndex(index+1)
      setIsBack(true);
    }
  }

  useEffect(() => {
    if (Object.keys(result).length > 0 && !isBack) {
      setResultHistory((prevHistory) => [result, ...prevHistory]);
    }
  }, [result]);

  const resetIndex = ()=>{
    setIndex(-1);
  }
  const handleSetDataRerank = (data) => {
    dataRerank = data;
  };

  const handleRerank = async () => {
    setIsSubmitting(true);
    const response = await fetch("http://127.0.0.1:8000/rerank", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(dataRerank),
    });
    const json = await response.json();
    setResult(json);
    setIndex(0);
    setIsBack(false);
    setIsSubmitting(false);
  };

  const handleSubmit = async (data) => {
    const stages = Object.values(JSON.parse(JSON.stringify(data)));
    const stagesBody = [];
    for (let stage of stages) {
      let count = 0;
      for (let type in stage.data) {
        if (type === "object") continue;
        if (stage.data[type]) count++;
        else {
          delete stage.data[type];
        }
      }
      if (count != 1) {
        alert(
          "Each type has to have one type from scene or image, text, speech, sketch"
        );
        return;
      }
      const type = Object.keys(stage.data)[0];
      const data = stage.data[type];
      const objectInput = stage.data["object"];
      let object;
      if (objectInput) {
        object = {};
        let group = Object.groupBy(objectInput, (object) => object.object);
        for (let obj in group) {
          const elm = group[obj].map((elm) => elm.offset);
          object[obj] = elm;
        }
      }
      const lang = stage["lang"];
      stagesBody.push({ type, data, object, lang });
    }

    const body = { stages: stagesBody, K: K };

    setIsSubmitting(true);
    const response = await fetch("http://127.0.0.1:8000/", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(body),
    });
    const json = await response.json();
    setResult(json);
    setIndex(0);
    setIsBack(false);
    setIsSubmitting(false);
  };

  return (
    <div className="App flex flex-row overflow-hidden relative">
      {!open && <IconButton 
            label="Open"
            className="border-2 border-teal-500 hover:bg-teal-500 hover:text-white mx-auto mt-4 absolute left-2"
            onClick={() => setOpen(true)}
        >
             <GoArrowRight className='text-2xl'/>
        </IconButton>}
      <SearchBar
        onSubmit={handleSubmit}
        isSubmitting={isSubmitting}
        K={K}
        onChangeK={setK}
        onRerank={handleRerank}
        open={open}
        setOpen={setOpen}
      />
      <Result onChangeDataRerank={handleSetDataRerank} result={result} K={K} onGoBack={BacktoResult} onClear={resetIndex}/>
    </div>
  );
}

export default App;

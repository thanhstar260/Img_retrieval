import SearchBar from './layouts/SearchBar';
import { useState } from 'react';
import Result from './layouts/Result';

function App() {
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (data) => {
    console.log("hello")
    const body = Object.values(data);
    console.log(body);

    //fetch ????? TODO
    // simulation
    setIsSubmitting(true);
    await (new Promise((resolve) => setTimeout(resolve, 2000)))
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

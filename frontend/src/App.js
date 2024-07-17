import logo from './logo.svg';
import SearchBar from './layouts/SearchBar';
import { useState } from 'react';

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
    <div className="App">
      <SearchBar onSubmit={handleSubmit} isSubmitting={isSubmitting}/>
    </div>
    
  );
}

export default App;

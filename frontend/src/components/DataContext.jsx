import React, { createContext, useState } from 'react';

const DataContext = createContext();

const MyProvider = ({ children }) => {
  const [ids, setIds] = useState([]);
  const [dis, setDis] = useState([]);

  return (
    <DataContext.Provider value={{ ids, setIds, dis, setDis }}>
      {children}
    </DataContext.Provider>
  );
};

export { DataContext, MyProvider };

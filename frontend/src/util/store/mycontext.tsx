import React from 'react';
import { createUtilStore } from './utilstore';
import { createUserStore } from './userstore';
import { createShowStore } from './showstore';
import { useLocalObservable } from 'mobx-react-lite';;

const MyShowsContext = React.createContext({
    utilStore: undefined,
    userStore: undefined,
    showStore: undefined,
});

export const MyShowsProvider: React.FC<{}> = ( {children} ) => {
    const utilStore = useLocalObservable(createUtilStore);
    const userStore = useLocalObservable(createUserStore);
    const showStore = useLocalObservable(createShowStore)
    
    return (
        <MyShowsContext.Provider value={{ utilStore, userStore, showStore }}>
            {children}
        </MyShowsContext.Provider>
    );
};

export const useStore = () => React.useContext(MyShowsContext)
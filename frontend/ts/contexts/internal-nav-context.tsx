import React, {
  createContext,
  useContext,
  useState,
  useCallback,
} from "react";

export interface NavItem {
  id: string;
  component: React.ComponentType<any>;
  props: any;
  title: string;
}

interface InternalNavContextType {
  stack: NavItem[];
  push: (
    component: React.ComponentType<any>,
    title: string,
    props?: any
  ) => void;
  pop: () => void;
  goToIndex: (index: number) => void;
}

const InternalNavContext = createContext<InternalNavContextType | undefined>(
  undefined
);

export const InternalNavProvider = ({
  children,
  initialPage,
  initialTitle,
}: {
  children: React.ReactNode;
  initialPage: React.ComponentType<any>;
  initialTitle: string;
}) => {
  const [stack, setStack] = useState<NavItem[]>([
    { id: "root", component: initialPage, title: initialTitle, props: {} },
  ]);

  const push = useCallback(
    (component: React.ComponentType<any>, title: string, props: any = {}) => {
      const id = Math.random().toString(36).substring(7);
      setStack((prev) => [...prev, { id, component, title, props }]);
    },
    []
  );

  const pop = useCallback(() => {
    setStack((prev) => (prev.length > 1 ? prev.slice(0, -1) : prev));
  }, []);

  const goToIndex = useCallback((index: number) => {
    setStack((prev) => prev.slice(0, index + 1));
  }, []);

  return (
    <InternalNavContext.Provider value={{ stack, push, pop, goToIndex }}>
      {children}
    </InternalNavContext.Provider>
  );
};

export const useInternalNav = () => {
  const context = useContext(InternalNavContext);
  if (!context)
    throw new Error("useInternalNav must be used within InternalNavProvider");
  return context;
};

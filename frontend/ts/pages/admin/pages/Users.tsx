import { useState, type ReactNode } from "react";
import { columns } from "../components/user-column";
import { DataTable } from "../components/data-table";
import DashboardLayout from "../DashboardLayout";

import type {
  ColumnFiltersState,
  SortingState,
  PaginationState,
} from "@tanstack/react-table";
import { roles_systeme, statuses } from "../data/user";
import { useDebounce } from "@uidotdev/usehooks";
import { useGetUsers } from "@/api/users";




function UsersPage() {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [pagination, setPagination] = useState<PaginationState>({ pageIndex: 0, pageSize: 10 });
  const debounceColumnFilters = useDebounce(
    columnFilters,
    300
  );
  
  const {isLoading, data} = useGetUsers({columnFilters: debounceColumnFilters, pagination})
  
  return (
    <div className="@container/main flex-1 flex-col space-y-8 p-8 md:flex">
      <div className="flex items-center justify-between space-y-2">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Welcome back!</h2>
          <p className="text-muted-foreground">
            Here&apos;s a list of your tasks for this month!
          </p>
        </div>
        <div className="flex items-center space-x-2">{/* <UserNav /> */}</div>
      </div>
    
      <DataTable
        paginatedDataTable={
          {
            data: data.items,
            total_filtered: data?.meta.total_items
          }
        }
        loading={isLoading}
        columns={columns}
        sorting={sorting}
        setSorting={setSorting}
        columnFilters={columnFilters}
        setColumnFilters={setColumnFilters}
        pagination={pagination}
        setPagination={setPagination}
        config={
          {
            searchId: "search",
            searchPlaceholder: "Recherche par nom",
            filters: [
              {
                columnId: "role_systeme",
                title: "Role",
                options: roles_systeme,
              },
              {
                columnId: "est_actif",
                title: "Status",
                options: statuses,
              },
            ]
          }
        }
      /> 
    </div>
  );
}

UsersPage.layout = (page: ReactNode) => {
  return <DashboardLayout>{page}</DashboardLayout>;
};

export default UsersPage;

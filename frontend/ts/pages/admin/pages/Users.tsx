import { useEffect, useState, type ReactNode } from "react";
import { columns } from "../components/user-column";
import { DataTable } from "../components/data-table";
import DashboardLayout from "../DashboardLayout";

import type {
  ColumnFiltersState,
  SortingState,
  PaginationState,
} from "@tanstack/react-table";
import { roles_systeme, statuses } from "../data/user";
import axios from "@/lib/axios";


async function getUsers(
  pageIndex: number = 0,
  pageSize: number = 10,
  search: string = "",
) {
  try {
    const response = await axios.get(`/users/?page=${pageIndex + 1}&page_size=${pageSize}&search=${search}`);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

function UsersPage() {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [pagination, setPagination] = useState<PaginationState>({ pageIndex: 0, pageSize: 10 });
  const [data, setData] = useState<any>({ data: [], total_filtered: 0 });
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const effectKey = JSON.stringify({ sorting, columnFilters, pagination });
  useEffect(() => {
    const getAllTask = async () => {
      setIsLoading(true);
      const res = await getUsers(
        pagination.pageIndex,
        pagination.pageSize,
      );
      setData({
        data: res.items,
        total_filtered: res.meta.total_items
      });
      setIsLoading(false);
    }
    getAllTask();
  }, [effectKey]);

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
          data
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
            searchColumnId: "nom_complet",
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

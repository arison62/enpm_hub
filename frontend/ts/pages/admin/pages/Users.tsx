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
import { UserManagementDialogs } from "../components/user-management-dialog";
import { Upload, UserPlus } from "lucide-react";
import { Button } from "@/components/ui/button";




function UsersPage() {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [pagination, setPagination] = useState<PaginationState>({ pageIndex: 0, pageSize: 10 });
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showImportDialog, setShowImportDialog] = useState(false);

  const debounceColumnFilters = useDebounce(
    columnFilters,
    300
  );
  
  const {isLoading, data, error, refetch} = useGetUsers({columnFilters: debounceColumnFilters, pagination})
  const handleUserCreated = () => {
    refetch()
    setShowCreateDialog(false)
  }
  const handleUsersImported = () => {
    refetch()
    setShowImportDialog(false)
  }
    console.log("data : ", data);
  return (
    <div className="@container/main flex-1 flex-col space-y-8 p-8 md:flex">
      <div className="flex items-center justify-between space-y-2">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">
            Gestion des utilisateur
          </h2>
          <p className="text-muted-foreground">
            Gérez les utilisateurs de votre application
          </p>
        </div>
        <div className="flex flex-col items-start gap-2 md:flex-row items-center space-x-2">
          <Button variant="outline" onClick={() => setShowImportDialog(true)}>
            <Upload className="mr-2 h-4 w-4" />
            Importer
          </Button>
          <Button onClick={() => setShowCreateDialog(true)}>
            <UserPlus className="mr-2 h-4 w-4" />
            Créer un utilisateur
          </Button>
        </div>
      </div>
      {error && <p>{error.message}</p>}
      <DataTable
        paginatedDataTable={{
          data: data.items,
          total_filtered: data?.meta.total_items,
        }}
        loading={isLoading}
        columns={columns}
        sorting={sorting}
        setSorting={setSorting}
        columnFilters={columnFilters}
        setColumnFilters={setColumnFilters}
        pagination={pagination}
        setPagination={setPagination}
        config={{
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
          ],
        }}
      />
      <UserManagementDialogs
        showCreateDialog={showCreateDialog}
        setShowCreateDialog={setShowCreateDialog}
        showImportDialog={showImportDialog}
        setShowImportDialog={setShowImportDialog}
        onUserCreated={handleUserCreated}
        onUsersImported={handleUsersImported}
      />
    </div>
  );
}

UsersPage.layout = (page: ReactNode) => {
  return <DashboardLayout>{page}</DashboardLayout>;
};

export default UsersPage;

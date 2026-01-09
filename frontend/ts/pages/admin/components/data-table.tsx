import * as React from "react";
import {
  type ColumnDef,
  type ColumnFiltersState,
  type SortingState,
  type VisibilityState,
  type PaginationState,
  flexRender,
  getCoreRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getPaginationRowModel,
  useReactTable,
  getFilteredRowModel,
  getSortedRowModel,
} from "@tanstack/react-table";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { DataTablePagination } from "./data-table-pagination";
import { DataTableToolbar } from "./data-table-toolbar";
import { useEffect } from "react";
import type { LucideIcon } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";


interface DataTableConfig<TData> {
  searchId: string
  searchPlaceholder?: string;
  filters: Array<{
    columnId: keyof TData & string;
    title: string;
    options: {
      label: string;
      value: string | boolean;
      icon?: LucideIcon;
    }[];
  }>;
}
interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  paginatedDataTable: {
    data: TData[];
    total_filtered: number;
  };
  sorting?: SortingState;
  loading: boolean;
  setSorting?: React.Dispatch<React.SetStateAction<SortingState>>;
  columnFilters?: ColumnFiltersState;
  setColumnFilters?: React.Dispatch<React.SetStateAction<ColumnFiltersState>>;
  pagination?: PaginationState;
  setPagination?: React.Dispatch<React.SetStateAction<PaginationState>>;
  config: DataTableConfig<TData>;
}

export function DataTable<TData, TValue>({
  columns,
  paginatedDataTable,
  sorting,
  setSorting,
  columnFilters,
  setColumnFilters,
  pagination,
  setPagination,
  loading,
  config,
}: DataTableProps<TData, TValue>) {
  const [rowSelection, setRowSelection] = React.useState({});
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({});

  //   const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
  //     []
  //   );
  //   const [sorting, setSorting] = React.useState<SortingState>([]);

  // eslint-disable-next-line react-hooks/incompatible-library
  const table = useReactTable({
    data: paginatedDataTable.data,
    columns,
    // sort configuration
    onSortingChange: setSorting,
    enableMultiSort: false,
    manualSorting: true,
    sortDescFirst: true,

    // filter configuration
    onColumnFiltersChange: setColumnFilters,
    manualFiltering: true,

    // pagination configuration
    getPaginationRowModel: getPaginationRowModel(),
    onPaginationChange: setPagination,
    rowCount: paginatedDataTable.total_filtered,
    pageCount: Math.ceil(
      (paginatedDataTable.total_filtered ?? 0) / (pagination?.pageSize ?? 1)
    ),
    manualPagination: true,
    state: {
      sorting,
      columnVisibility,
      rowSelection,
      columnFilters,
      pagination,
    },

    enableRowSelection: true,
    onRowSelectionChange: setRowSelection,
    onColumnVisibilityChange: setColumnVisibility,
    getCoreRowModel: getCoreRowModel(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
    getFilteredRowModel: getFilteredRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });
  // reset page index to 0 when filters change
  useEffect(() => {
    if (setPagination) {
      setPagination((prev) => ({
        ...prev,
        pageIndex: 0,
      }));
    }
  }, [columnFilters, setPagination]);

  return (
    <div className="space-y-4">
      <DataTableToolbar
        table={table}
        search={{
          filterId: config.searchId,
          placeholder: config.searchPlaceholder,
        }}
        filters={config.filters}
      />
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id} colSpan={header.colSpan}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {loading ? (
              Array.from({ length: pagination?.pageSize ?? 10 }).map(
                (_, rowIndex) => (
                  <TableRow key={`skeleton-row-${rowIndex}`}>
                    {columns.map((_, cellIndex) => (
                      <TableCell key={`skeleton-cell-${rowIndex}-${cellIndex}`}>
                        <Skeleton className="h-4 w-full" />
                      </TableCell>
                    ))}
                  </TableRow>
                )
              )
            ) : table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <DataTablePagination table={table} />
    </div>
  );
}

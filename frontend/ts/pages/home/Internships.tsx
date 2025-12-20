import AppLayout from "@/components/layouts/app-layout"
import type { ReactNode } from "react"

function InternshipsPage(){
    return <div className="flex flex-col h-full items-center space-y-8">
        <h1 className="text-2xl font-bold">Internships</h1>
        <div>
            Internships page qui va presenter les offre de stage
        </div>
    </div>
}

InternshipsPage.layout = (page : ReactNode) => <AppLayout>{page}</AppLayout>
export default InternshipsPage;

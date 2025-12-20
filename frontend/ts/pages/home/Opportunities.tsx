import AppLayout from "@/components/layouts/app-layout"
import type { ReactNode } from "react"

function OpportunitesPage(){
    return <div className="flex flex-col h-full items-center space-y-8">
        <h1 className="text-2xl font-bold">Opportunites</h1>
        <div>
            Opportunites page qui va presenter les formation et les offre d'emploie ...
        </div>
    </div>
}

OpportunitesPage.layout = (page : ReactNode) => <AppLayout>{page}</AppLayout>
export default OpportunitesPage;

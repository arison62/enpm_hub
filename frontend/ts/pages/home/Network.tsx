import AppLayout from "@/components/layouts/app-layout"
import type { ReactNode } from "react"

function NetworkPage(){
    return <div className="flex flex-col h-full items-center space-y-8">
        <h1 className="text-2xl font-bold">Network</h1>
        <div>
            Network page qui va presenter les personnes et les partenaires de l'ENSPM
        </div>
    </div>
}

NetworkPage.layout = (page : ReactNode) => <AppLayout>{page}</AppLayout>
export default NetworkPage;

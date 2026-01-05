import enspmLogo from "@/assets/enspm-logo.png";
import PasswordResetForm from "./components/password-reset-form";

export default function PasswordResetPage() {
  return (
    <div className="grid min-h-svh">
      <div className="flex flex-col gap-4 p-6 md:p-10">
        <div className="flex justify-center gap-2 md:justify-start">
          <a href="#" className="flex items-center gap-2 font-medium">
            <div className="flex items-center justify-center rounded-md">
              <img src={enspmLogo} alt="ENSPM Hub" className="h-10" />
            </div>
            ENSPM Hub
          </a>
        </div>
        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-xs">
            <PasswordResetForm />
          </div>
        </div>
      </div>
    </div>
  );
}

import Image from "next/image";
import Link from "next/link";

export default function HomePage() {
  return (
    <main className="justify-center items-center flex flex-col min-h-screen">
      <Image
        src={"/x3-logo.webp"}
        alt="x3"
        width={100}
        height={100}
        className="rounded-full shadow-2xl mb-3"
      ></Image>
      <h1 className="mb-4 text-2xl font-bold">x3</h1>
      <p className="text-fd-muted-foreground">A fishing-centered economy bot</p>
      <p className="text-fd-muted-foreground">
        See{" "}
        <Link
          href="/docs"
          className="text-fd-foreground font-semibold underline"
        >
          /docs
        </Link>{" "}
        for the documentation.
      </p>
    </main>
  );
}

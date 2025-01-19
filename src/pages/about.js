import Head from "next/head";
import Link from "next/link";
import { ArrowLeft as ArrowLeftIcon } from "lucide-react";

import appName from "./index";

export default function About() {
  return (
    <div>
      <Head>
        <title>{appName}</title>
      </Head>

      <main className="container max-w-[600px] mx-auto p-5">
        <h1 className="text-center text-5xl font-bold m-6">{appName}</h1>

        <p className="prose">
          This open-source website provides a simple interface for changing the language of your favorite memes. You can upload an image, select your target language, and generate new
          memes based on your selection.
        </p>

        <p className="prose">
          The translation model is {" "}
          <Link href="https://replicate.com/timothybrooks/instruct-pix2pix?utm_source=project&utm_campaign=paintbytext">
            Gemini
          </Link>
          , which exposes a cloud API for running predictions. This website is
          built with Next.js and hosted on
          <Link href="https://vercel.com/templates/ai">Vercel</Link>. The source code
          is publicly available on{" "}
          <Link href="https://github.com/XiaohanYa/meme_lingo">
            GitHub
          </Link>
          . Pull requests welcome!
        </p>

        <div className="text-center mt-10">
          <Link
            href="/"
            className="bg-black text-white rounded-md text-small inline-block p-3 flex-none">

            <ArrowLeftIcon className="icon" />Back to Meme
          </Link>
        </div>
      </main>
    </div>
  );
}

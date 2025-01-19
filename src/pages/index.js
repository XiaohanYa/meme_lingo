import Messages from "components/messages";
import PromptForm from "components/prompt-form";
import Head from "next/head";
import { useEffect, useState } from "react";

import Footer from "components/footer";

import prepareImageFileForUpload from "lib/prepare-image-file-for-upload";
import { getRandomSeed } from "lib/seeds";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export const appName = "Meme Lingo";
export const appSubtitle = "Your Fun Meme Translator.";
export const appMetaDescription = "Translate your favorite memes into any language.";

export default function Home() {
  const [events, setEvents] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [error, setError] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [seed] = useState(getRandomSeed());
  const [initialPrompt, setInitialPrompt] = useState("Select a language (e.g., Spanish, French, German)");

  // Remove or comment out this useEffect if you don't want any initial image
  // useEffect(() => {
  //   setEvents([{ image: seed.image }]);
  // }, [seed.image]);

  const handleImageDropped = async (image) => {
    try {
      image = await prepareImageFileForUpload(image);
    } catch (error) {
      setError(error.message);
      return;
    }
    setEvents(events.concat([{ image }]));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const prompt = e.target.prompt.value;
    const lastImage = events.findLast((ev) => ev.image)?.image;

    setError(null);
    setIsProcessing(true);
    setInitialPrompt("");

    const myEvents = [...events, { prompt }];
    setEvents(myEvents);

    // Create FormData to send file
    const formData = new FormData();
    
    // Convert base64/URL image to blob if needed
    let imageBlob;
    try {
        if (lastImage.startsWith('data:')) {
            console.log('Converting base64 image to blob');
            const response = await fetch(lastImage);
            imageBlob = await response.blob();
        } else {
            console.log('Converting URL image to blob');
            const response = await fetch(lastImage);
            imageBlob = await response.blob();
        }
        console.log('Image blob created:', imageBlob.size, 'bytes');
        
        // Append the file and target language to FormData
        formData.append('file', imageBlob, 'image.png');
        formData.append('target_language', prompt);
        
        console.log('FormData contents:');
        for (let pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }
    } catch (error) {
        console.error('Error preparing image:', error);
        setError('Error preparing image: ' + error.message);
        setIsProcessing(false);
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/translate", {
            method: "POST",
            body: formData,
        });
        
        const result = await response.json();
        console.log('Translation result:', result);

        if (!response.ok) {
            setError(result.detail || 'Translation failed');
            setIsProcessing(false);
            return;
        }

        const updatedEvents = myEvents.concat([
            { 
                type: 'assistant',
                translation: result.translation 
            }
        ]);
        console.log('Updated events:', updatedEvents);
        setEvents(updatedEvents);
        
    } catch (error) {
        console.error('Translation error:', error);
        setError(error.message);
    } finally {
        setIsProcessing(false);
    }
  };

  const startOver = async (e) => {
    e.preventDefault();
    setEvents([]);
    setError(null);
    setIsProcessing(false);
    setInitialPrompt("Select a language (e.g., Spanish, French, German)");
  };

  return (
    <div>
      <Head>
        <title>{appName}</title>
        <meta name="description" content={appMetaDescription} />
        <meta property="og:title" content={appName} />
        <meta property="og:description" content={appMetaDescription} />
        <meta property="og:image" content="https://paintbytext.chat/opengraph.jpg" />
      </Head>

      <main className="container max-w-[700px] mx-auto p-5">
        <hgroup>
          <h1 className="text-center text-5xl font-bold m-6">{appName}</h1>
          <p className="text-center text-xl opacity-60 m-6">
            {appSubtitle}
          </p>
        </hgroup>

        <Messages
          events={events}
          isProcessing={isProcessing}
          onUndo={(index) => {
            setInitialPrompt(events[index - 1].prompt);
            setEvents(
              events.slice(0, index - 1).concat(events.slice(index + 1))
            );
          }}
        />

        <PromptForm
          initialPrompt={initialPrompt}
          isFirstPrompt={events.length === 1}
          onSubmit={handleSubmit}
          disabled={isProcessing}
        />

        <div className="mx-auto w-full">
          {error && <p className="bold text-red-500 pb-5">{error}</p>}
        </div>

        <Footer
          events={events}
          startOver={startOver}
          handleImageDropped={handleImageDropped}
        />
      </main>
    </div>
  );
}

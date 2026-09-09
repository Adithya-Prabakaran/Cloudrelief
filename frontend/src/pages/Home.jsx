import { Link } from "react-router-dom";
import { Button, Card, Eyebrow } from "../components/ui";
import SeverityBadge from "../components/SeverityBadge";

export default function Home() {
  return (
    <div className="relative mx-auto max-w-page overflow-hidden px-6 pb-32 pt-8 sm:px-10">
      <div className="pointer-events-none absolute -right-24 top-0 h-72 w-72 rounded-full bg-peach/60 blur-3xl" />

      <section className="relative mx-auto max-w-2xl text-center">
        <Eyebrow className="justify-center">Disaster response, simplified</Eyebrow>
        <h1 className="mt-4 text-[44px] leading-[1.05] tracking-tighter text-ink sm:text-[64px]">
          Every report,
          <br />
          one shared map.
        </h1>
        <p className="mx-auto mt-5 max-w-md text-[15px] leading-relaxed text-graphite">
          Citizens report incidents in seconds. CloudRelief scores severity from the
          photo, the description, and what else is happening nearby&nbsp;&mdash; so admins
          know what to act on first.
        </p>
        <div className="mt-9 flex flex-wrap items-center justify-center gap-3">
          <Button as={Link} to="/login" variant="primary">
            Citizen Portal
          </Button>
          <Button as={Link} to="/admin/login" variant="ghost">
            Admin Portal
          </Button>
        </div>
      </section>

      <section className="relative mt-20 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <Card className="shadow-float">
          <Eyebrow>Live incident</Eyebrow>
          <p className="mt-3 font-serif text-lg text-ink">Flooding, Elm St.</p>
          <div className="mt-3 flex items-center justify-between">
            <span className="text-xs text-graphite">2 min ago</span>
            <SeverityBadge score={0.78} />
          </div>
        </Card>

        <Card accent className="shadow-float">
          <Eyebrow className="text-sienna/70">How it's scored</Eyebrow>
          <p className="mt-3 font-serif text-lg">Photo + words + density</p>
          <p className="mt-3 text-sm text-sienna/80">
            One weighted formula turns a report into a number admins can triage by.
          </p>
        </Card>

        <Card className="shadow-float">
          <Eyebrow>Response time</Eyebrow>
          <p className="mt-3 font-serif text-4xl tracking-tighter text-ink">6.4x</p>
          <p className="mt-2 text-sm text-graphite">faster team assignment vs. manual intake</p>
        </Card>
      </section>
    </div>
  );
}

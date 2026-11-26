interface Props {
  title: string;
  text: string;
}

export function Placeholder({ title, text }: Props) {
  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold tracking-tight text-navy">{title}</h1>
      <p className="mt-3 rounded-xl border border-dashed border-slate-300 bg-white p-8 text-slate-500">{text}</p>
    </div>
  );
}

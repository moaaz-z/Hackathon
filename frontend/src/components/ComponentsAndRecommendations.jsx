import {
  FileCode2,
  Lightbulb,
} from "lucide-react";

export function KeyComponents({
  components = [],
}) {
  return (
    <section className="panel">
      <div className="section-heading">
        <span className="eyebrow">
          Key Components
        </span>

        <h2>Important Project Areas</h2>
      </div>

      <div className="stack-list">
        {components.length > 0 ? (
          components.map((item, index) => {
            const name =
              typeof item === "string"
                ? item
                : item?.name ||
                  item?.file ||
                  item?.path ||
                  "Component";

            const description =
              typeof item === "object"
                ? item?.description ||
                  item?.purpose ||
                  item?.role ||
                  ""
                : "";

            return (
              <article
                className="component-card"
                key={index}
              >
                <FileCode2 size={18} />

                <div>
                  <strong>{name}</strong>

                  {item?.file && (
                    <code>{item.file}</code>
                  )}

                  {description && (
                    <p>{description}</p>
                  )}
                </div>
              </article>
            );
          })
        ) : (
          <p className="muted">
            No key components returned.
          </p>
        )}
      </div>
    </section>
  );
}

export function Recommendations({
  recommendations = [],
}) {
  return (
    <section className="panel">
      <div className="section-heading">
        <span className="eyebrow">
          Recommendations
        </span>

        <h2>Action Plan</h2>
      </div>

      <div className="stack-list">
        {recommendations.length > 0 ? (
          recommendations.map((item, index) => (
            <article
              className="recommendation-card"
              key={index}
            >
              <div className="recommendation-number">
                {index + 1}
              </div>

              <div>
                <strong>
                  {typeof item === "string"
                    ? item
                    : item?.title ||
                      "Recommendation"}
                </strong>

                {typeof item === "object" &&
                  item?.priority && (
                    <span className="priority-pill">
                      {item.priority}
                    </span>
                  )}

                {typeof item === "object" &&
                  item?.description && (
                    <p>{item.description}</p>
                  )}
              </div>

              <Lightbulb size={17} />
            </article>
          ))
        ) : (
          <p className="muted">
            No recommendations returned.
          </p>
        )}
      </div>
    </section>
  );
}